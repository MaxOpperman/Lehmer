<script setup lang="ts">
import * as d3 from 'd3';
import { onMounted, ref, watch } from 'vue';

interface Node extends d3.SimulationNodeDatum {
  id: number;
  trailing: number[];
  subsignature: number[];
}

interface Edge {
  key: string; // The key representing the edge (e.g., "[[1, 2], [2, 2]]")
  source: number; // The ID of the source node
  target: number; // The ID of the target node
  value: string; // The concatenated value of the edge
  curvature: number; // Curvature for the edge
}

// Props
const props = defineProps<{
  nodes: Node[];
  edges: Record<string, any>;
}>();

const graphContainer = ref<HTMLDivElement | null>(null);

const drawGraph = () => {
  if (!graphContainer.value) return;

  // Clear previous graph
  d3.select(graphContainer.value).selectAll('*').remove();

  const width = '80vw';
  const height = '70vh';

  const svg = d3
    .select(graphContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  // Tooltip for edge hover
  const tooltip = d3
    .select(graphContainer.value)
    .append('div')
    .style('position', 'absolute')
    .style('background', '#fff')
    .style('border', '1px solid #ccc')
    .style('padding', '5px')
    .style('border-radius', '5px')
    .style('pointer-events', 'none')
    .style('display', 'none');

  // Map trailing values to node IDs for edge lookup
  const trailingToNodeId = new Map(
    props.nodes.map((node) => [JSON.stringify(node.trailing), node.id])
  );

  // Transform edges to use node IDs with swapping logic
  const transformedEdges = Object.entries(props.edges)
    .flatMap(([key, edgeData]) => {
      const [sourceTrailing, targetTrailing] = JSON.parse(key.replace(/'/g, '"'));

      // Generate all possible edges based on the edge data
      const possibleEdges: Edge[] = [];
      const sourceId = trailingToNodeId.get(JSON.stringify(sourceTrailing));
      const targetId = trailingToNodeId.get(JSON.stringify(targetTrailing));

      if (sourceId !== undefined && targetId !== undefined) {
        edgeData.forEach((pair: any, index: number) => {
          const [firstArray, secondArray] = pair;

          // Add two edges for each pair with curvature
          possibleEdges.push({
            key: `${key}-${index}-0`,
            source: sourceId,
            target: targetId,
            value: `${firstArray[0].join('')} - ${secondArray[0].join('')}`,
            curvature: 0.2, // Slight curvature for differentiation
          });
          possibleEdges.push({
            key: `${key}-${index}-1`,
            source: sourceId,
            target: targetId,
            value: `${firstArray[1].join('')} - ${secondArray[1].join('')}`,
            curvature: -0.2, // Opposite curvature for differentiation
          });
        });
      }

      // Handle swapping logic for trailing values
      const swappedSourceTrailing = [...sourceTrailing].reverse();
      const swappedTargetTrailing = [...targetTrailing].reverse();

      const swappedSourceId = trailingToNodeId.get(JSON.stringify(swappedSourceTrailing));
      const swappedTargetId = trailingToNodeId.get(JSON.stringify(swappedTargetTrailing));

      if (swappedSourceId !== undefined && targetId !== undefined) {
        edgeData.forEach((pair: any, index: number) => {
          const [firstArray, secondArray] = pair;

          // Add two edges for swapped source
          possibleEdges.push({
            key: `${key}-swapped-${index}-0`,
            source: swappedSourceId,
            target: targetId,
            value: `${firstArray[0].join('')} - ${secondArray[0].join('')}`,
            curvature: 0.2,
          });
          possibleEdges.push({
            key: `${key}-swapped-${index}-1`,
            source: swappedSourceId,
            target: targetId,
            value: `${firstArray[1].join('')} - ${secondArray[1].join('')}`,
            curvature: -0.2,
          });
        });
      }

      if (sourceId !== undefined && swappedTargetId !== undefined) {
        edgeData.forEach((pair: any, index: number) => {
          const [firstArray, secondArray] = pair;

          // Add two edges for swapped target
          possibleEdges.push({
            key: `${key}-swapped-target-${index}-0`,
            source: sourceId,
            target: swappedTargetId,
            value: `${firstArray[0].join('')} - ${secondArray[0].join('')}`,
            curvature: 0.2,
          });
          possibleEdges.push({
            key: `${key}-swapped-target-${index}-1`,
            source: sourceId,
            target: swappedTargetId,
            value: `${firstArray[1].join('')} - ${secondArray[1].join('')}`,
            curvature: -0.2,
          });
        });
      }

      return possibleEdges;
    });

  // Calculate maximum node size for spacing
  const maxNodeRadius = Math.max(
    ...props.nodes.map((node) => Math.max(30, node.subsignature.join(', ').length * 5))
  );

  const simulation = d3
    .forceSimulation(props.nodes)
    .force(
      'link',
      d3.forceLink(transformedEdges)
        .id((d: any) => d.id)
        .distance(maxNodeRadius * 2) // Adjust distance based on node size
    )
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(
      graphContainer.value.clientWidth / 2,
      graphContainer.value.clientHeight / 2
    ));

  const link = svg
    .append('g')
    .selectAll('path')
    .data(transformedEdges)
    .enter()
    .append('path')
    .attr('stroke', '#999')
    .attr('stroke-width', 4) // Increased stroke width for larger edges
    .attr('fill', 'none')
    .attr('d', (d: any) => {
      const curvature = d.curvature || 0;
      return `M${d.source.x},${d.source.y} Q${(d.source.x + d.target.x) / 2 + curvature * 100},${(d.source.y + d.target.y) / 2 + curvature * 100} ${d.target.x},${d.target.y}`;
    })
    .on('mouseover', (event: MouseEvent, d: any) => {
      tooltip
        .style('display', 'block')
        .style('left', `${event.pageX + 10}px`)
        .style('top', `${event.pageY + 10}px`)
        .style('color', '#333')
        .html(`<strong>Edge Value:</strong> ${d.value}`);
    })
    .on('mouseout', () => {
      tooltip.style('display', 'none');
    });

  const nodeGroup = svg
    .append('g')
    .selectAll('g')
    .data(props.nodes)
    .enter()
    .append('g')
    .call(
      d3
        .drag<SVGGElement, Node>()
        .on('start', (event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on('drag', (event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on('end', (event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        })
    );

  // Append circles to represent nodes
  nodeGroup
    .append('circle')
    .attr('r', (d: any) => Math.max(30, d.subsignature.join(', ').length * 5)) // Adjust radius based on text length
    .attr('fill', 'steelblue');

  // Append text inside nodes to display subsignature and trailing items
  nodeGroup
    .append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '-0.5em') // Position the first line slightly above the center
    .attr('fill', 'white')
    .text((d: any) => d.subsignature.join(', '));

  nodeGroup
    .append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '1em') // Position the second line slightly below the center
    .attr('fill', 'white')
    .text((d: any) => `_${d.trailing.join('')}`);

  simulation.on('tick', () => {
    link.attr('d', (d: any) => {
      const curvature = d.curvature || 0;
      return `M${d.source.x},${d.source.y} Q${(d.source.x + d.target.x) / 2 + curvature * 100},${(d.source.y + d.target.y) / 2 + curvature * 100} ${d.target.x},${d.target.y}`;
    });

    nodeGroup.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
  });
};

onMounted(() => {
  drawGraph();
});

watch(() => [props.nodes, props.edges], () => {
  drawGraph();
});
</script>

<template>
  <div>
    <h2>Graph Visualization</h2>
    <div ref="graphContainer" style="border: 1px solid #ddd;"></div>
  </div>
</template>

<style scoped>
svg {
  background-color: #f9f9f9;
}

div {
  font-family: Arial, sans-serif;
}
</style>