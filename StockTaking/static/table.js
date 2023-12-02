function capatalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

class Table {
    constructor(parent, table_name, headers, data) {
        this.table_name = table_name;
        this.headers = headers;
        this.data = data;

        this.table_container = parent;
        this.table = null;

        this.init();
    }

    init() {
        this.draw_table_view();
    }

    draw_table_view() {
        this.table_container.innerHTML = '';

        // Create Table Elements
        this.table = document.createElement('table');
        let table_head = document.createElement('thead');
        let table_body = document.createElement('tbody');

        this.table.classList.add('table');
        this.table.classList.add(this.table_name);

        /* Construct Header Row */
        let table_head_row = document.createElement('tr');
        this.headers.forEach(header => {
            let table_head_cell = document.createElement('th');
            table_head_cell.innerHTML = `${capatalize(header)}`;
            table_head_row.appendChild(table_head_cell);    
        })
        table_head.appendChild(table_head_row);

        /* Construct Table Body */
        this.data.forEach(row => {
            let table_body_row = document.createElement('tr');
            let row_id = row[0];

            this.headers.forEach((header, index) => {
                let table_body_cell = document.createElement('td');
                let cell_value = row[index];

                table_body_cell.innerHTML = cell_value;
                table_body_cell.setAttribute('data-id', row_id);
                table_body_cell.setAttribute('data-key', header);
                table_body_cell.setAttribute('data-value', cell_value);

                table_body_row.appendChild(table_body_cell);
            })

            table_body.appendChild(table_body_row);
        })

        this.table.appendChild(table_head);
        this.table.appendChild(table_body);

        this.table_container.appendChild(this.table);
    }

    get_headers() {
        return this.headers;
    }

    get_data() {
        return this.data;
    }

}