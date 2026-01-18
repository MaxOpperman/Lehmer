<script setup lang="ts">
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";
import {
  BackendEdgeData,
  type Edge,
  NodeWithPosition,
  type VisualizationNode,
  generateEdges,
} from "../utils/edgeGenerator";

// Props
const props = defineProps<{
  nodes: VisualizationNode[];
  edges: BackendEdgeData | undefined;
  accumulatedLength: number;
}>();

// Emit event for node click
const emit = defineEmits<{
  (e: "node-clicked", subsignature: number[], trailing: number[]): void;
}>();

const graphContainer = ref<HTMLDivElement | null>(null);

const drawGraph = () => {
  if (!graphContainer.value || !props.edges) return;

  // Clear previous graph
  d3.select(graphContainer.value).selectAll("*").remove();

  const width = graphContainer.value.clientWidth;
  const height = graphContainer.value.clientHeight;

  const svg = d3
    .select(graphContainer.value)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const zoom = d3
    .zoom<SVGSVGElement, unknown>()
    .scaleExtent([0.1, 4]) // Allow more zoom out
    .on("zoom", (event) => {
      containerGroup.attr("transform", event.transform);
    });

  svg.call(zoom);

  const containerGroup = svg.append("g"); // Group for panning and zooming

  // Tooltip for edge hover
  const tooltip = d3
    .select(graphContainer.value)
    .append("div")
    .style("position", "absolute")
    .style("background", "#fff")
    .style("border", "1px solid #ccc")
    .style("padding", "5px")
    .style("border-radius", "5px")
    .style("pointer-events", "none")
    .style("display", "none");

  // Generate edges using the utility function
  const transformedEdges: Edge[] = generateEdges(props.nodes, props.edges, props.accumulatedLength);

  // Calculate maximum node size for spacing
  // Smaller nodes for large graphs to fit more on screen
  const baseRadius = props.nodes.length > 50 ? 20 : 30;
  const maxNodeRadius = Math.max(
    ...props.nodes.map((node) =>
      Math.max(baseRadius, node.subsignature.join(", ").length * 3),
    ),
  );

  // Ensure nodes conform to SimulationNodeDatum
  const nodesWithDatum = (props.nodes as NodeWithPosition[]).map((node) => ({
    ...node,
    x: node.x ?? 0,
    y: node.y ?? 0,
    vx: node.vx ?? 0,
    vy: node.vy ?? 0,
  }));

  // Scale spacing based on number of nodes - smaller graphs get more space
  const nodeCount = props.nodes.length;
  let linkDistance, chargeStrength, collisionPadding;
  
  if (nodeCount < 10) {
    linkDistance = maxNodeRadius * 4;
    chargeStrength = -300;
    collisionPadding = 10;
  } else if (nodeCount < 30) {
    linkDistance = maxNodeRadius * 3;
    chargeStrength = -200;
    collisionPadding = 5;
  } else if (nodeCount < 100) {
    linkDistance = maxNodeRadius * 1.5;
    chargeStrength = -100;
    collisionPadding = 2;
  } else {
    linkDistance = maxNodeRadius * 1.2;
    chargeStrength = -50;
    collisionPadding = 1;
  }
  
  const simulation = d3
    .forceSimulation(nodesWithDatum)
    .force(
      "link",
      d3
        .forceLink(transformedEdges)
        .id((d: d3.SimulationNodeDatum) => (d as VisualizationNode).id)
        .distance(linkDistance),
    )
    .force("charge", d3.forceManyBody().strength(chargeStrength))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(maxNodeRadius + collisionPadding));

  const link = containerGroup
    .append("g")
    .selectAll("path")
    .data(transformedEdges)
    .enter()
    .append("path")
    .attr("stroke", "#999")
    .attr("stroke-width", 1.5)
    .attr("fill", "none")
    .attr("d", (d: Edge) => {
      const curvature = d.curvature || 0;
      // If d.source or d.target is a number, find the corresponding node object
      const source: NodeWithPosition =
        typeof d.source === "number"
          ? nodesWithDatum.find((n) => n.id === d.source)!
          : (d.source as NodeWithPosition);
      const target: NodeWithPosition =
        typeof d.target === "number"
          ? nodesWithDatum.find((n) => n.id === d.target)!
          : (d.target as NodeWithPosition);
      const sx = source.x ?? 0;
      const sy = source.y ?? 0;
      const tx = target.x ?? 0;
      const ty = target.y ?? 0;
      return `M${sx},${sy} Q${(sx + tx) / 2 + curvature * 100},${(sy + ty) / 2 + curvature * 100} ${tx},${ty}`;
    })
    .on("mouseover", (event: MouseEvent, d: Edge) => {
      tooltip
        .style("display", "block")
        .style("left", `${event.pageX + 10}px`)
        .style("top", `${event.pageY + 10}px`)
        .style("color", "#333")
        .html(`<strong>Edge:</strong> ${d.value}`);
    })
    .on("mouseout", () => {
      tooltip.style("display", "none");
    });

  const nodeGroup = containerGroup
    .append("g")
    .selectAll("g")
    .data(nodesWithDatum)
    .enter()
    .append("g")
    .call(
      d3
        .drag<
          SVGGElement,
          NodeWithPosition & { fx?: number | null; fy?: number | null }
        >()
        .on("start", (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }),
    );

  // Append circles to represent nodes
  const nodeRadius = props.nodes.length > 50 ? 20 : 30;
  nodeGroup
    .append("circle")
    .attr("r", (d: NodeWithPosition) =>
      Math.max(nodeRadius, d.subsignature.join(", ").length * 3),
    )
    .attr("fill", "steelblue")
    .on("click", (event, d: NodeWithPosition) => {
      // Extract only the original backend trailing (not the accumulated part)
      const originalTrailing = d.trailing.slice(0, d.trailing.length - props.accumulatedLength);
      emit("node-clicked", d.subsignature, originalTrailing); // Emit the subsignature and original trailing
    });

  // Append text inside nodes to display subsignature and trailing items
  const fontSize = props.nodes.length > 50 ? "10px" : "12px";
  nodeGroup
    .append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "-0.5em")
    .attr("fill", "white")
    .attr("font-size", fontSize)
    .attr("font-weight", "bold")
    .style("user-select", "none")
    .text((d: NodeWithPosition) => `(${d.subsignature.join(", ")})`);

  nodeGroup
    .append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "1em")
    .attr("fill", "white")
    .attr("font-size", props.nodes.length > 50 ? "9px" : "11px")
    .style("user-select", "none")
    .text((d: NodeWithPosition & { permutation?: number[] }) => {
      // Show permutation if available (full graph mode), otherwise show trailing
      if (d.permutation && d.permutation.length > 0) {
        return d.permutation.join("");
      }
      return `_${d.trailing.join("")}`;
    });

  simulation.on("tick", () => {
    link.attr("d", (d: Edge) => {
      const curvature = d.curvature || 0;
      // If d.source or d.target is a number, find the corresponding node object
      const source: NodeWithPosition =
        typeof d.source === "number"
          ? nodesWithDatum.find((n) => n.id === d.source)!
          : (d.source as NodeWithPosition);
      const target: NodeWithPosition =
        typeof d.target === "number"
          ? nodesWithDatum.find((n) => n.id === d.target)!
          : (d.target as NodeWithPosition);
      const sx = source.x ?? 0;
      const sy = source.y ?? 0;
      const tx = target.x ?? 0;
      const ty = target.y ?? 0;
      return `M${sx},${sy} Q${(sx + tx) / 2 + curvature * 100},${(sy + ty) / 2 + curvature * 100} ${tx},${ty}`;
    });

    nodeGroup.attr(
      "transform",
      (d: NodeWithPosition) => `translate(${d.x},${d.y})`,
    );
  });

  // After simulation ends, zoom to fit all nodes
  simulation.on("end", () => {
    if (nodesWithDatum.length === 0) return;
    
    // Calculate bounds of all nodes
    const xExtent = d3.extent(nodesWithDatum, d => d.x ?? 0) as [number, number];
    const yExtent = d3.extent(nodesWithDatum, d => d.y ?? 0) as [number, number];
    
    const padding = maxNodeRadius * 3; // Add padding around the graph
    const graphWidth = xExtent[1] - xExtent[0] + padding * 2;
    const graphHeight = yExtent[1] - yExtent[0] + padding * 2;
    
    // Calculate scale to fit graph in viewport
    const scale = Math.min(
      width / graphWidth,
      height / graphHeight,
      1 // Don't zoom in beyond 1x
    ) * 0.9; // 90% to leave some margin
    
    // Calculate translation to center the graph
    const translateX = width / 2 - (xExtent[0] + xExtent[1]) / 2 * scale;
    const translateY = height / 2 - (yExtent[0] + yExtent[1]) / 2 * scale;
    
    // Apply the transform
    svg.call(
      zoom.transform as any,
      d3.zoomIdentity.translate(translateX, translateY).scale(scale)
    );
  });
};

onMounted(() => {
  drawGraph();
});

watch(
  () => [props.nodes, props.edges, props.accumulatedLength],
  () => {
    drawGraph();
  },
);
</script>

<template>
  <div>
    <h2>Graph Visualization</h2>
    <div ref="graphContainer" class="graph-container"></div>
  </div>
</template>

<style scoped>
.graph-container {
  width: 100%;
  min-width: 50vw;
  height: 70vh;
  border: 1px solid #ddd;
  overflow: hidden;
}

svg {
  background-color: #f9f9f9;
}

div {
  font-family: Arial, sans-serif;
}
</style>
