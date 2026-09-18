(function () {
    const form = document.getElementById("shorten-form");
    const urlInput = document.getElementById("url-input");
    const shortenButton = document.getElementById("shorten-btn");
    const result = document.getElementById("result");
    const error = document.getElementById("error");
    const linksBody = document.getElementById("links-body");

    function displayError(message) {
        error.textContent = message;
    }

    async function readResponse(response) {
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.error || data.message || "Request failed");
        }

        return data;
    }

    async function loadLinks() {
        try {
            const response = await fetch("/api/links");
            const data = await readResponse(response);
            const links = Array.isArray(data) ? data : (data.links || []);

            linksBody.textContent = "";

            links.forEach(function (link) {
                const row = document.createElement("tr");
                const codeCell = document.createElement("td");
                const urlCell = document.createElement("td");
                const clicksCell = document.createElement("td");

                codeCell.textContent = link.code || "";
                urlCell.textContent = link.url || "";
                clicksCell.textContent = link.clicks ?? 0;

                row.appendChild(codeCell);
                row.appendChild(urlCell);
                row.appendChild(clicksCell);
                linksBody.appendChild(row);
            });
        } catch (requestError) {
            displayError(requestError.message);
        }
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        result.textContent = "";
        error.textContent = "";
        shortenButton.disabled = true;

        try {
            const response = await fetch("/api/shorten", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: urlInput.value })
            });
            const data = await readResponse(response);
            const link = document.createElement("a");

            link.href = data.short_url;
            link.textContent = data.short_url;
            link.target = "_blank";
            link.rel = "noopener noreferrer";

            result.appendChild(link);
            urlInput.value = "";
            await loadLinks();
        } catch (requestError) {
            displayError(requestError.message);
        } finally {
            shortenButton.disabled = false;
        }
    });

    loadLinks();
}());
