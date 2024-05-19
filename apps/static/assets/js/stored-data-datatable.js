const MAX_PROPERTY_TITLE_LENGTH = 20;
let nextPage = 2;
let dataTable;

window.addEventListener('DOMContentLoaded', event => {
    const storedDataTable = document.getElementById('storedDataTable');
    const loadMoreBtn = document.getElementById('load-more-btn');
    const showPreviousBtn = document.getElementById('show-previous-btn');

    initializeDataTable(storedDataTable); // Initialize DataTable on page load

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            pushNewTable(storedDataTable);
        });
    }

    if (showPreviousBtn) {
        showPreviousBtn.addEventListener('click', () => {
            loadPreviousPage(storedDataTable);
        });
    }
});

function pushNewTable(storedDataTable) {
    if (storedDataTable) {
        fetch(`?page=${nextPage}`)
            .then(response => response.text())
            .then(html => {
                console.log(html)
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newTableBody = doc.querySelector('#storedDataTable tbody');

                const fragment = document.createDocumentFragment();

                newTableBody.querySelectorAll('tr').forEach(row => {
                    fragment.appendChild(row);
                });

                storedDataTable.querySelector('tbody').appendChild(fragment);

                nextPage++;

                initializeDataTable(storedDataTable);

                const loadMoreContainer = document.getElementById('load-more-container');
                if (nextPage > 2 && !loadMoreContainer.querySelector('#show-previous-btn')) {
                    const prevButton = document.createElement('button');
                    prevButton.id = 'show-previous-btn';
                    prevButton.textContent = 'Show Previous Data';
                    prevButton.addEventListener('click', () => {
                        loadPreviousPage(storedDataTable);
                    });
                    loadMoreContainer.appendChild(prevButton);
                } else if (nextPage <= 2 && loadMoreContainer.querySelector('#show-previous-btn')) {
                    // Remove "Show Previous Data" button if nextPage <= 2
                    loadMoreContainer.querySelector('#show-previous-btn').remove();
                }
            });
    }
}

function loadPreviousPage(storedDataTable) {
    nextPage = Math.max(nextPage - 2, 2);
    pushNewTable(storedDataTable);
}

function initializeDataTable(tableElement) {
    let options = {
        searchable: true,
        perPageSelect: [10, 20, 50, 100, 500, 1000],
        labels: {
            placeholder: "Search...",
            searchTitle: "Search within properties",
            perPage: "per page",
            noRows: "No properties to display",
            info: "Showing {end} entries from total of {rows}",
        },
        columns: [
            {
                select: 0,
                type: 'string',
                render: function (data, td, rowIndex, cellIndex) {
                    if (data.length > MAX_PROPERTY_TITLE_LENGTH) {
                        return '<span id="PropertyTitle" class="truncated" title="' + data + '">' + data.substr(0, MAX_PROPERTY_TITLE_LENGTH) + '...</span>';
                    } else {
                        return data;
                    }
                }
            },
            {
                select: 1,
                type: 'string',
                render: function (data, td, rowIndex, cellIndex) {
                    const district = data.split("-")[1];
                    return `${district.charAt(0).toUpperCase() + district.slice(1)}`;
                }
            },
            {
                select: 3,
                type: 'string',
                render: function (data, td, rowIndex, cellIndex) {
                    switch (true) {
                        case data.includes("dom"):
                            return "Rodinný dom";
                        case data.includes("izbový  byt"):
                            return data.charAt(0) + "-iz. byt";
                        default:
                            return data;
                    }
                    return `${district.charAt(0).toUpperCase() + district.slice(1)}`;
                }
            }
        ]
    };

    // Destroy previous SimpleDatatables instance (if exists)
    if (dataTable) {
        dataTable.destroy();
    }

    // Initialize SimpleDatatables
    dataTable = new simpleDatatables.DataTable(tableElement, options);
}
