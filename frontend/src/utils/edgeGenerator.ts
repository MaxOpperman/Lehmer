export interface Node extends d3.SimulationNodeDatum {
  id: number;
  trailing: number[];
  subsignature: number[];
}

export interface Edge {
  key: string; // The key representing the edge
  source: number; // The ID of the source node
  target: number; // The ID of the target node
  value: string; // The concatenated value of the edge
  curvature: number; // Curvature for the edge
}

export const generateEdges = (
  nodes: { id: number; trailing: number[] }[],
  edges: Record<string, any>,
): Edge[] => {
  const trailingToNodeId = new Map(
    nodes.map((node) => [JSON.stringify(node.trailing), node.id]),
  );

  const transformedEdges = Object.entries(edges).flatMap(([key, edgeData]) => {
    const [sourceTrailing, targetTrailing] = JSON.parse(key.replace(/'/g, '"'));

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
          value: `${firstArray[0].join("")} - ${secondArray[0].join("")}`,
          curvature: 0.2,
        });
        possibleEdges.push({
          key: `${key}-${index}-1`,
          source: sourceId,
          target: targetId,
          value: `${firstArray[1].join("")} - ${secondArray[1].join("")}`,
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
      edgeData.forEach((pair: any, index: number) => {
        const [firstArray, secondArray] = pair;

        possibleEdges.push({
          key: `${key}-swapped-${index}-0`,
          source: swappedSourceId,
          target: targetId,
          value: `${firstArray[0].join("")} - ${secondArray[0].join("")}`,
          curvature: 0.2,
        });
        possibleEdges.push({
          key: `${key}-swapped-${index}-1`,
          source: swappedSourceId,
          target: targetId,
          value: `${firstArray[1].join("")} - ${secondArray[1].join("")}`,
          curvature: -0.2,
        });
      });
    }

    if (sourceId !== undefined && swappedTargetId !== undefined) {
      edgeData.forEach((pair: any, index: number) => {
        const [firstArray, secondArray] = pair;

        possibleEdges.push({
          key: `${key}-swapped-target-${index}-0`,
          source: sourceId,
          target: swappedTargetId,
          value: `${firstArray[0].join("")} - ${secondArray[0].join("")}`,
          curvature: 0.2,
        });
        possibleEdges.push({
          key: `${key}-swapped-target-${index}-1`,
          source: sourceId,
          target: swappedTargetId,
          value: `${firstArray[1].join("")} - ${secondArray[1].join("")}`,
          curvature: -0.2,
        });
      });
    }

    return possibleEdges;
  });

  return transformedEdges;
};
