<script setup lang="ts">
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";
import {
  BackendEdge,
  type Edge,
  NodeWithPosition,
  type VisualizationNode,
  generateEdges,
} from "../utils/edgeGenerator";

// Props
const props = defineProps<{
  nodes: VisualizationNode[];
  edges: BackendEdge | undefined;
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
    .attr("height", height)
    .call(
      d3
        .zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.5, 2]) // Set zoom limits
        .on("zoom", (event) => {
          svg.select("g").attr("transform", event.transform);
        }),
    );

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
  const maxNodeRadius = Math.max(
    ...props.nodes.map((node) =>
      Math.max(30, node.subsignature.join(", ").length * 4.5),
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

  const simulation = d3
    .forceSimulation(nodesWithDatum)
    .force(
      "link",
      d3
        .forceLink(transformedEdges)
        .id((d: d3.SimulationNodeDatum) => (d as VisualizationNode).id)
        .distance(maxNodeRadius * 2), // Adjust distance based on node size
    )
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(maxNodeRadius + 5)); // Add collision force

  const link = containerGroup
    .append("g")
    .selectAll("path")
    .data(transformedEdges)
    .enter()
    .append("path")
    .attr("stroke", "#999")
    .attr("stroke-width", 4) // Increased stroke width for larger edges
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
  nodeGroup
    .append("circle")
    .attr("r", (d: NodeWithPosition) =>
      Math.max(30, d.subsignature.join(", ").length * 4.25),
    ) // Adjust radius based on text length
    .attr("fill", "steelblue")
    .on("click", (event, d: NodeWithPosition) => {
      // Extract only the original backend trailing (not the accumulated part)
      const originalTrailing = d.trailing.slice(0, d.trailing.length - props.accumulatedLength);
      emit("node-clicked", d.subsignature, originalTrailing); // Emit the subsignature and original trailing
    });

  // Append text inside nodes to display subsignature and trailing items
  nodeGroup
    .append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "-0.5em") // Position the first line slightly above the center
    .attr("fill", "white")
    .style("user-select", "none") // Make text non-selectable
    .text((d: NodeWithPosition) => `(${d.subsignature.join(", ")})`);

  nodeGroup
    .append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "1em") // Position the second line slightly below the center
    .attr("fill", "white")
    .style("user-select", "none") // Make text non-selectable
    .text((d: NodeWithPosition) => `_${d.trailing.join("")}`); // Display trailing elements

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
