<script setup lang="ts">
import { ref } from 'vue';
import GraphVisualization from './components/GraphVisualization.vue';

const API_BASE_URL = 'http://127.0.0.1:5000'; // Update for production if needed
const signatureInput = ref('');
const nodes = ref([]);
const edges = ref([]);
const errorMessage = ref('');

const fetchVisualization = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/visualize_cycles`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ signature: signatureInput.value.split(',').map(Number) }),
    });
    const data = await response.json();

    console.log('Response from backend:', data);
    if (data.error) {
      errorMessage.value = data.error;
      nodes.value = [];
      edges.value = [];
    } else {
      nodes.value = data.nodes;
      edges.value = data.edges;
      errorMessage.value = '';
    }
    console.log('Nodes:', JSON.stringify(nodes.value));
    console.log('Edges:', JSON.stringify(edges.value));
  } catch (error) {
    errorMessage.value = 'Failed to fetch data from the backend.';
  }
};
</script>

<template>
  <div id="app">
    <h1>Graph Visualization</h1>
    <form @submit.prevent="fetchVisualization">
      <label for="signature">Enter Signature (comma-separated):</label>
      <input v-model="signatureInput" id="signature" required />
      <button type="submit">Generate</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <GraphVisualization :nodes="nodes" :edges="edges" />
  </div>
</template>

<style>
body {
  margin: 0;
  padding: 20px;
}

h1 {
  text-align: center;
}

form {
  text-align: center;
}

.error {
  color: red;
  text-align: center;
}
</style>