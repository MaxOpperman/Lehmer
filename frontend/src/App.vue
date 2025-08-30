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

// Computed property to format edges for display
const formattedEdges = computed(() => {
  const transformedEdges = generateEdges(nodes.value, edges.value);
  return transformedEdges.map((edge) => {
    const sourceNode = nodes.value.find((node) => node.id === edge.source);
    const targetNode = nodes.value.find((node) => node.id === edge.target);

    if (sourceNode && targetNode) {
      return {
        subsignature: `(${sourceNode.subsignature.join(",")})`,
        boldPart: `${sourceNode.trailing.join("")}/${targetNode.trailing.join("")}`,
        value: `: ${edge.value}`,
      };
    }
    return {
      subsignature: "",
      boldPart: "",
      value: edge.value,
    };
  });
});

const fetchVisualization = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/visualize_cycles`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        signature: signatureInput.value.split(",").map(Number),
      }),
    });
    const data = await response.json();

    if (data.error) {
      errorMessage.value = data.error;
      nodes.value = [];
      edges.value = undefined;
    } else {
      nodes.value = data.nodes;
      edges.value = data.edges;
      errorMessage.value = "";
    }
  } catch (error) {
    errorMessage.value = "Failed to fetch data from the backend.";
    console.error(error);
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
    <form @submit.prevent="fetchVisualization">
      <label for="signature">Enter Signature (comma-separated):</label>
      <input id="signature" v-model="signatureInput" required />
      <button type="submit">Generate</button>
    </form>
    <p v-if="errorMessage" class="error">
      {{ errorMessage }}
    </p>
    <div class="content">
      <GraphVisualization :nodes="nodes" :edges="edges" />
      <button class="toggle-button" @click="isSidebarOpen = !isSidebarOpen">
        {{ isSidebarOpen ? "Hide Edges" : "Show Edges" }}
      </button>
      <div class="sidebar" :class="{ open: isSidebarOpen }">
        <ul v-if="isSidebarOpen" class="edge-list">
          <li v-for="(edge, index) in formattedEdges" :key="index">
            <span>{{ edge.subsignature }}</span>
            <strong>{{ edge.boldPart }}</strong>
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

.edge-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.edge-list li {
  margin: 0.5rem 0;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.visualization {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}
</style>
