import { z } from "zod";

export const VisualizationNodeSchema = z.object({
  id: z.number(),
  trailing: z.array(z.number()),
  subsignature: z.array(z.number()),
  permutation: z.array(z.number()).optional(), // For full graphs
});

export type VisualizationNode = z.infer<typeof VisualizationNodeSchema>;

export const NodeWithPositionSchema = VisualizationNodeSchema.extend({
  x: z.number(),
  y: z.number(),
  vx: z.number(),
  vy: z.number(),
});

export type NodeWithPosition = z.infer<typeof NodeWithPositionSchema>;

export const EdgeSchema = z.object({
  key: z.string(),
  source: z.number(),
  target: z.number(),
  value: z.string(),
  curvature: z.number(),
});

export type Edge = z.infer<typeof EdgeSchema>;

export type BackendEdge = {
  [key: string]: [[number[], number[]], [number[], number[]]];
};

export type SimpleEdge = {
  source: number;
  target: number;
};

export type BackendEdgeData = BackendEdge | SimpleEdge[];

const constructEdgeValue = (
  firstArray: number[],
  secondArray: number[],
): string => {
  const firstValue = Array.isArray(firstArray[0])
    ? (firstArray[0] as number[]).join("")
    : String(firstArray[0]);
  const secondValue = Array.isArray(secondArray[0])
    ? (secondArray[0] as number[]).join("")
    : String(secondArray[0]);
  return `${firstValue} - ${secondValue}`;
};

// Helper function to extract original trailing values from the backend
const getOriginalTrailing = (fullTrailing: number[], accumulatedLength: number): number[] => {
  // The original trailing is everything except the last accumulatedLength elements
  return fullTrailing.slice(0, fullTrailing.length - accumulatedLength);
};

export const generateEdges = (
  nodes: { id: number; trailing: number[] }[],
  edges: BackendEdgeData | undefined,
  accumulatedLength: number = 0,
): Edge[] => {
  if (!edges) return [];

  // Check if this is a simple edge list (full graph format)
  if (Array.isArray(edges)) {
    return generateSimpleEdges(edges);
  }

  // Otherwise, use the cross-edge format
  return generateCrossEdges(nodes, edges, accumulatedLength);
};

// Handle simple edge list format (for full neighbor-swap graphs)
const generateSimpleEdges = (edges: SimpleEdge[]): Edge[] => {
  return edges.map((edge, index) => ({
    key: `edge-${index}`,
    source: edge.source,
    target: edge.target,
    value: "", // No value for simple edges
    curvature: 0,
  }));
};

// Handle cross-edge format (for cycle-cover based graphs)
const generateCrossEdges = (
  nodes: { id: number; trailing: number[] }[],
  edges: BackendEdge,
  accumulatedLength: number,
): Edge[] => {

  // Create a map using original trailing values (without accumulated trailing)
  const originalTrailingToNodeId = new Map(
    nodes.map((node) => {
      const originalTrailing = getOriginalTrailing(node.trailing, accumulatedLength);
      return [JSON.stringify(originalTrailing), node.id];
    })
  );

  const transformedEdges = Object.entries(edges).flatMap(([key, edgeData]) => {
    const [sourceTrailing, targetTrailing] = JSON.parse(key.replace(/'/g, '"'));

    const possibleEdges: Edge[] = [];
    const sourceId = originalTrailingToNodeId.get(JSON.stringify(sourceTrailing));
    const targetId = originalTrailingToNodeId.get(JSON.stringify(targetTrailing));

    if (sourceId !== undefined && targetId !== undefined) {
      edgeData.forEach((pair, index) => {
        const [firstArray, secondArray] = pair;

        // Add two edges for each pair with curvature
        possibleEdges.push({
          key: `${key}-${index}-0`,
          source: sourceId,
          target: targetId,
          value: constructEdgeValue(firstArray, secondArray), // Use helper function
          curvature: 0.2,
        });
        possibleEdges.push({
          key: `${key}-${index}-1`,
          source: sourceId,
          target: targetId,
          value: constructEdgeValue(firstArray.slice(1), secondArray.slice(1)), // Use helper function
          curvature: -0.2,
        });
      });
    }

    // Handle swapping logic for trailing values
    const swappedSourceTrailing = [...sourceTrailing].reverse();
    const swappedTargetTrailing = [...targetTrailing].reverse();

    const swappedSourceId = originalTrailingToNodeId.get(
      JSON.stringify(swappedSourceTrailing),
    );
    const swappedTargetId = originalTrailingToNodeId.get(
      JSON.stringify(swappedTargetTrailing),
    );

    if (swappedSourceId !== undefined && targetId !== undefined) {
      edgeData.forEach((pair, index: number) => {
        const [firstArray, secondArray] = pair;

        possibleEdges.push({
          key: `${key}-swapped-${index}-0`,
          source: swappedSourceId,
          target: targetId,
          value: constructEdgeValue(firstArray, secondArray), // Use helper function
          curvature: 0.2,
        });
        possibleEdges.push({
          key: `${key}-swapped-${index}-1`,
          source: swappedSourceId,
          target: targetId,
          value: constructEdgeValue(firstArray.slice(1), secondArray.slice(1)), // Use helper function
          curvature: -0.2,
        });
      });
    }

    if (sourceId !== undefined && swappedTargetId !== undefined) {
      edgeData.forEach((pair, index: number) => {
        const [firstArray, secondArray] = pair;

        possibleEdges.push({
          key: `${key}-swapped-target-${index}-0`,
          source: sourceId,
          target: swappedTargetId,
          value: constructEdgeValue(firstArray, secondArray), // Use helper function
          curvature: 0.2,
        });
        possibleEdges.push({
          key: `${key}-swapped-target-${index}-1`,
          source: sourceId,
          target: swappedTargetId,
          value: constructEdgeValue(firstArray.slice(1), secondArray.slice(1)), // Use helper function
          curvature: -0.2,
        });
      });
    }

    return possibleEdges;
  });

  return transformedEdges;
};
