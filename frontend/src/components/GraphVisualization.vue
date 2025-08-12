<script setup lang="ts">
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";
import { type Edge, type Node, generateEdges } from "../utils/edgeGenerator";

// Props
const props = defineProps<{
  nodes: Node[];
  edges: Record<string, any>;
}>();

const graphContainer = ref<HTMLDivElement | null>(null);

const drawGraph = () => {
  if (!graphContainer.value) return;

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
  const transformedEdges: Edge[] = generateEdges(props.nodes, props.edges);

  // Calculate maximum node size for spacing
  const maxNodeRadius = Math.max(
    ...props.nodes.map((node) =>
      Math.max(30, node.subsignature.join(", ").length * 4),
    ),
  );

  const simulation = d3
    .forceSimulation(props.nodes)
    .force(
      "link",
      d3
        .forceLink(transformedEdges)
        .id((d: any) => d.id)
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
    .attr("d", (d: any) => {
      const curvature = d.curvature || 0;
      return `M${d.source.x},${d.source.y} Q${(d.source.x + d.target.x) / 2 + curvature * 100},${(d.source.y + d.target.y) / 2 + curvature * 100} ${d.target.x},${d.target.y}`;
    })
    .on("mouseover", (event: MouseEvent, d: any) => {
      tooltip
        .style("display", "block")
        .style("left", `${event.pageX + 10}px`)
        .style("top", `${event.pageY + 10}px`)
        .html(`<strong>Edge:</strong> ${d.value}`);
    })
    .on("mouseout", () => {
      tooltip.style("display", "none");
    });

  const nodeGroup = containerGroup
    .append("g")
    .selectAll("g")
    .data(props.nodes)
    .enter()
    .append("g")
    .call(
      d3
        .drag<SVGGElement, Node>()
        .on(
          "start",
          (event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          },
        )
        .on(
          "drag",
          (event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) => {
            d.fx = event.x;
            d.fy = event.y;
          },
        )
        .on(
          "end",
          (event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          },
        ),
    );

  // Append circles to represent nodes
  nodeGroup
    .append("circle")
    .attr("r", (d: any) => Math.max(30, d.subsignature.join(", ").length * 3.5)) // Adjust radius based on text length
    .attr("fill", "steelblue");

  // Append text inside nodes to display subsignature and trailing items
  nodeGroup
    .append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "-0.5em") // Position the first line slightly above the center
    .attr("fill", "white")
    .text((d: any) => d.subsignature.join(", "));

  nodeGroup
    .append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "1em") // Position the second line slightly below the center
    .attr("fill", "white")
    .text((d: any) => `_${d.trailing.join("")}`);

  simulation.on("tick", () => {
    link.attr("d", (d: any) => {
      const curvature = d.curvature || 0;
      return `M${d.source.x},${d.source.y} Q${(d.source.x + d.target.x) / 2 + curvature * 100},${(d.source.y + d.target.y) / 2 + curvature * 100} ${d.target.x},${d.target.y}`;
    });

    nodeGroup.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
  });
};

onMounted(() => {
  drawGraph();
});

watch(
  () => [props.nodes, props.edges],
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
