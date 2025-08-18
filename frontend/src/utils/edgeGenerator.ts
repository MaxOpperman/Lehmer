import { z } from "zod";

export const VisualizationNodeSchema = z.object({
  id: z.number(),
  trailing: z.array(z.number()),
  subsignature: z.array(z.number()),
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
  [key: string]: [[number[], number[]], [number[], number[]]]
}

const constructEdgeValue = (firstArray: number[], secondArray: number[]): string => {
  const firstValue = Array.isArray(firstArray[0]) ? (firstArray[0] as number[]).join("") : String(firstArray[0]);
  const secondValue = Array.isArray(secondArray[0]) ? (secondArray[0] as number[]).join("") : String(secondArray[0]);
  return `${firstValue} - ${secondValue}`;
};

export const generateEdges = (
  nodes: { id: number; trailing: number[] }[],
  edges: BackendEdge | undefined,
): Edge[] => {
  if (!edges) return [];

  const trailingToNodeId = new Map(
    nodes.map((node) => [JSON.stringify(node.trailing), node.id]),
  );

  const transformedEdges = Object.entries(edges).flatMap(([key, edgeData]) => {
    const [sourceTrailing, targetTrailing] = JSON.parse(key.replace(/'/g, '"'));

    const possibleEdges: Edge[] = [];
    const sourceId = trailingToNodeId.get(JSON.stringify(sourceTrailing));
    const targetId = trailingToNodeId.get(JSON.stringify(targetTrailing));

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

    const swappedSourceId = trailingToNodeId.get(
      JSON.stringify(swappedSourceTrailing),
    );
    const swappedTargetId = trailingToNodeId.get(
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
