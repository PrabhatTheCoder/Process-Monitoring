const spinner = document.getElementById("spinner");
const errorMsg = document.getElementById("errorMsg");
const tbody = document.querySelector("#hostTable tbody");

// Function to handle snapshot click
function goToSnapshot(hostId, hostName) {
    localStorage.setItem('selectedHost', JSON.stringify({id: hostId, name: hostName}));
    window.location.href = '/snapshot/';
}

async function loadHosts() {
    spinner.style.display = "block";
    errorMsg.textContent = "";
    try {
        const res = await fetch(`${API_BASE_URL}/api/available-host/`);
        if (!res.ok) throw new Error("Failed to fetch hosts");
        const data = await res.json();

        tbody.innerHTML = "";
        data.forEach(host => {
            const row = `
                <tr>
                    <td>${host.name}</td>
                    <td>${new Date(host.created_at).toLocaleString()}</td>
                    <td><button class="btn btn-primary"><a href="/live/${encodeURIComponent(host.name)}/">Live Status</a></button></td>
                    <td><button class="btn btn-primary" onclick="goToSnapshot('${host.id}', '${host.name}')">System Snapshot</button></td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (err) {
        errorMsg.textContent = err.message;
    } finally {
        spinner.style.display = "none";
    }
}
loadHosts();