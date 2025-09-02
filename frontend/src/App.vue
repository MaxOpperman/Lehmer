<script setup lang="ts">
import { computed, ref } from "vue";
import GraphVisualization from "./components/GraphVisualization.vue";
import {
  BackendEdge,
  generateEdges,
  VisualizationNode,
} from "./utils/edgeGenerator";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5050";

const signatureInput = ref("");
const nodes = ref<VisualizationNode[]>([]);
const edges = ref<BackendEdge | undefined>(undefined);
const errorMessage = ref("");
const isSidebarOpen = ref(true); // State for toggling the sidebar
const stack = ref<number[][]>([]); // Stack to store signature history
const stackTrailing = ref<number[][]>([]); // Stack to store trailing history
const currentStackIndex = ref(0); // Current position in the stack
const currentAccumulatedLength = ref(0); // Track the current accumulated trailing length

// Computed property to get the current subsignature
const currentSubsignature = computed(() =>
  stack.value[currentStackIndex.value] || null,
);

// Computed property to format edges for display
const formattedEdges = computed(() => {
  const transformedEdges = generateEdges(nodes.value, edges.value, currentAccumulatedLength.value);
  return transformedEdges.map((edge) => {
    const sourceNode = nodes.value.find((node) => node.id === edge.source);
    const targetNode = nodes.value.find((node) => node.id === edge.target);

    if (sourceNode && targetNode) {
      // Extract only the original backend trailing (without accumulated part)
      const sourceOriginalTrailing = sourceNode.trailing.slice(0, sourceNode.trailing.length - currentAccumulatedLength.value);
      const targetOriginalTrailing = targetNode.trailing.slice(0, targetNode.trailing.length - currentAccumulatedLength.value);
      
      // Extract the accumulated trailing part
      const accumulatedTrailing = stackTrailing.value[currentStackIndex.value] || [];
      const accumulatedTrailingStr = accumulatedTrailing.length > 0 ? accumulatedTrailing.join("") : "";
      
      return {
        subsignature: `(${sourceNode.subsignature.join(",")})`,
        boldPart: `${sourceOriginalTrailing.join("")}/${targetOriginalTrailing.join("")}`,
        italicPart: accumulatedTrailingStr ? `_${accumulatedTrailingStr}` : "",
        value: `: ${edge.value}`,
      };
    }
    return {
      subsignature: "",
      boldPart: "",
      italicPart: "",
      value: edge.value,
    };
  });
});

// Handle form submission to fetch the initial graph
const handleFormSubmit = async () => {
  const signature = signatureInput.value.split(",").map(Number);

  // Remove any forward history if navigating from the middle of the stack
  stack.value = stack.value.slice(0, currentStackIndex.value + 1);
  stackTrailing.value = stackTrailing.value.slice(0, currentStackIndex.value + 1);

  // Add the new signature to the stack
  stack.value.push(signature);
  stackTrailing.value.push([]); // No trailing for initial graph
  currentStackIndex.value = stack.value.length - 1; // Update the stack index

  currentAccumulatedLength.value = 0; // Reset accumulated length
  await fetchVisualization(signature, []);
};

// Handle node click to fetch a new graph
const handleNodeClick = async (subsignature: number[], trailing: number[]) => {
  // Remove any forward history if navigating from the middle of the stack
  stack.value = stack.value.slice(0, currentStackIndex.value + 1);
  stackTrailing.value = stackTrailing.value.slice(0, currentStackIndex.value + 1);

  stack.value.push(subsignature); // Add to stack
  
  // Prepend trailing: current node's trailing + previous trailing
  const currentTrailing = stackTrailing.value[currentStackIndex.value] || [];
  const newTrailing = [...trailing, ...currentTrailing]; // PREPEND the clicked node's trailing
  stackTrailing.value.push(newTrailing);
  
  currentStackIndex.value = stack.value.length - 1; // Update the stack index
  currentAccumulatedLength.value = newTrailing.length; // Update accumulated length

  // Fetch the new graph data from the backend
  await fetchVisualization(subsignature, newTrailing);
};

// Fetch graph visualization from the backend
const fetchVisualization = async (signature: number[], accumulatedTrailing: number[]) => {
  try {
    const response = await fetch(`${API_BASE_URL}/visualize_cycles`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        signature,
      }),
    });
    const data = await response.json();

    if (data.error) {
      errorMessage.value = data.error;
      nodes.value = [];
      edges.value = undefined;
    } else {
      // Update nodes and replace their trailing with: original backend trailing + accumulated trailing
      nodes.value = data.nodes.map((node: VisualizationNode) => {
        const originalBackendTrailing = node.trailing || [];
        return {
          ...node,
          trailing: [...originalBackendTrailing, ...accumulatedTrailing], // Backend trailing + accumulated trailing
        };
      });
      edges.value = data.edges;
      errorMessage.value = "";
      currentAccumulatedLength.value = accumulatedTrailing.length; // Update accumulated length
    }
  } catch (error) {
    errorMessage.value = "Failed to fetch data from the backend.";
    console.error(error);
  }
};

// Navigate backward in the stack
const goBack = async () => {
  if (currentStackIndex.value > 0) {
    currentStackIndex.value -= 1;
    const previousSignature = stack.value[currentStackIndex.value];
    const previousTrailing = stackTrailing.value[currentStackIndex.value] || [];
    currentAccumulatedLength.value = previousTrailing.length;
    await fetchVisualization(previousSignature, previousTrailing);
  }
};

// Navigate forward in the stack
const goForward = async () => {
  if (currentStackIndex.value < stack.value.length - 1) {
    currentStackIndex.value += 1;
    const nextSignature = stack.value[currentStackIndex.value];
    const nextTrailing = stackTrailing.value[currentStackIndex.value] || [];
    currentAccumulatedLength.value = nextTrailing.length;
    await fetchVisualization(nextSignature, nextTrailing);
  }
};
</script>

<template>
  <div id="app">
    <h1>Graph Visualization</h1>
    This website visualizes the meta-graph of cycles for given input signatures.
    What this exactly is is explained in
    <a
      href="/files/Lehmers_Conjecture_and_Hamiltonian_Paths_in_Neighbor_swap_Graphs.pdf"
      target="_blank"
      >the documentation</a
    >.
    <form @submit.prevent="handleFormSubmit">
      <label for="signature">Enter Signature (comma-separated):</label>
      <input id="signature" v-model="signatureInput" required />
      <button type="submit">Generate</button>
    </form>
    <p v-if="errorMessage" class="error">
      {{ errorMessage }}
    </p>
    <div class="content">
      <GraphVisualization
        :nodes="nodes"
        :edges="edges"
        :accumulated-length="currentAccumulatedLength"
        @node-clicked="(subsignature, trailing) => handleNodeClick(subsignature, trailing)"
      />
      <div v-if="currentSubsignature" class="current-subsig">
        <h3>Current Subsignature:</h3>
        <p>{{ currentSubsignature.join(", ") }}</p>
        <div v-if="stackTrailing[currentStackIndex] && stackTrailing[currentStackIndex].length > 0" class="current-trailing">
          <h4>Accumulated Trailing:</h4>
          <p>_{{ stackTrailing[currentStackIndex].join("") }}</p>
        </div>
        <button :disabled="currentStackIndex === 0" @click="goBack">
          Back
        </button>
        <button
          :disabled="currentStackIndex === stack.length - 1"
          @click="goForward"
        >
          Forward
        </button>
      </div>
      <button class="toggle-button" @click="isSidebarOpen = !isSidebarOpen">
        {{ isSidebarOpen ? "Hide Edges" : "Show Edges" }}
      </button>
      <div class="sidebar" :class="{ open: isSidebarOpen }">
        <ul v-if="isSidebarOpen" class="edge-list">
          <li v-for="(edge, index) in formattedEdges" :key="index">
            <span>{{ edge.subsignature }}</span>
            <strong>{{ edge.boldPart }}</strong>
            <em v-if="edge.italicPart">{{ edge.italicPart }}</em>
            <span>{{ edge.value }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

#app {
  max-width: 1280px;
  width: 80vw;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  margin-bottom: 1rem;
}

.error {
  margin-bottom: 1rem;
}

form {
  margin-bottom: 2rem;
}

.grid-container {
  display: grid;
  grid-template-rows: auto 1fr; /* Sidebar takes its height, visualization takes remaining space */
  gap: 1rem;
}

.sidebar {
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
  transform: translateY(-100%); /* Initially hidden above the visualization */
}

.sidebar.open {
  transform: translateY(0); /* Moves downwards when opened */
}

button {
  border: 1px solid #ddd;
  margin: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

button:disabled {
  color: #aaa;
  cursor: not-allowed;
}

.edge-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.edge-list li {
  margin: 0;
  padding: 0.3rem;
}

/* Add a line above every odd row (2n+1), except the first one */
.edge-list li:nth-child(2n+1):not(:first-child) {
  border-top: 0.2rem solid steelblue; /* Add a line between every second row */
}

.visualization {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

/* Add styles for the current subsignature display */
.current-subsig {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.current-trailing {
  margin-top: 0.5rem;
  font-style: italic;
  color: #666;
}
</style>
