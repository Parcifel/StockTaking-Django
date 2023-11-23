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

        this.table = document.createElement('table');
        this.table.classList.add('table');
        this.table.classList.add(this.table_name);

        let table_body = document.createElement('tdody');

        let table_head_row = document.createElement('tr');
        for (let i = 0; i < this.headers.length; i++) {
            let table_head_cell = document.createElement('th');
            table_head_cell.innerHTML = `${this.headers[i]}`;
            table_head_row.appendChild(table_head_cell);
        }
        table_body.appendChild(table_head_row);

        for (let row=0; row<this.data.length; row++) {
            let table_body_row = document.createElement('tr');
            let row_id = this.data[row][0];

            for (let col=0; col<this.headers.length; col++) {
                let table_body_cell = document.createElement('td');
                
                let cell_name = this.headers[col];
                let cell_value = this.data[row][col];

                table_body_cell.innerHTML = cell_value;
                table_body_cell.setAttribute('data-id', row_id);
                table_body_cell.setAttribute('data-key', cell_name);
                table_body_cell.setAttribute('data-value', cell_value);

                table_body_row.appendChild(table_body_cell);
            }
            table_body.appendChild(table_body_row);
        }

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