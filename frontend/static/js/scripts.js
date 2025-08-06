const form = document.getElementById('signature-form');
const visualization = document.getElementById('visualization');
const API_BASE_URL = window.API_BASE_URL || 'http://localhost:5000';

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const signature = document.getElementById('signature').value.split(',').map(Number);

    // Fetch visualization data from the backend
    const response = await fetch(`${API_BASE_URL}/visualize_cycles`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ signature })
    });
    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    visualizeCycles(data.nodes, data.edges);
});

function visualizeCycles(nodes, edges) {
    // Clear previous visualization
    visualization.innerHTML = '';

    const width = 800, height = 600;
    const svg = d3.select('#visualization')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // D3 expects source/target to be node objects, not indices
    const nodeMap = {};
    nodes.forEach(node => { nodeMap[node.id] = node; });
    const links = edges.map(e => ({
        source: nodeMap[e.source],
        target: nodeMap[e.target],
        detail: e.detail
    }));

    const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(200))
        .force('charge', d3.forceManyBody().strength(-400))
        .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
        .attr('stroke', '#999')
        .attr('stroke-opacity', 0.6)
        .selectAll('line')
        .data(links)
        .enter().append('line')
        .attr('stroke-width', 2);

    const node = svg.append('g')
        .attr('stroke', '#fff')
        .attr('stroke-width', 1.5)
        .selectAll('circle')
        .data(nodes)
        .enter().append('circle')
        .attr('r', 20)
        .attr('fill', 'steelblue')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    // Tooltip for node details
    node.append('title')
        .text(d => `Signature: ${d.signature}\nTrailing: ${d.trailing}`);

    // Optional: Show signature/trailing on hover as a floating tooltip
    node.on('mouseover', function(event, d) {
        d3.select(this).attr('fill', 'orange');
        showTooltip(event, `Signature: ${d.signature}<br>Trailing: ${d.trailing}`);
    }).on('mouseout', function() {
        d3.select(this).attr('fill', 'steelblue');
        hideTooltip();
    });

    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
    });

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    // Tooltip helpers
    function showTooltip(event, html) {
        let tooltip = document.getElementById('d3-tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.id = 'd3-tooltip';
            tooltip.style.position = 'absolute';
            tooltip.style.pointerEvents = 'none';
            tooltip.style.background = 'rgba(255,255,255,0.95)';
            tooltip.style.border = '1px solid #888';
            tooltip.style.padding = '8px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '14px';
            tooltip.style.zIndex = 1000;
            document.body.appendChild(tooltip);
        }
        tooltip.innerHTML = html;
        tooltip.style.left = (event.pageX + 10) + 'px';
        tooltip.style.top = (event.pageY + 10) + 'px';
        tooltip.style.display = 'block';
    }

    function hideTooltip() {
        const tooltip = document.getElementById('d3-tooltip');
        if (tooltip) tooltip.style.display = 'none';
    }
}