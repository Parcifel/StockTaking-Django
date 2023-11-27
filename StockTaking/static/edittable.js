function capatalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

class EditTable {
    constructor(parent, table_name, headers, types, data) {
        this.table_name = table_name;
        this.headers = headers;
        this.types = types;
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

        /* Header */
        let table_head_row = document.createElement('tr');
        for (let i = 0; i < this.headers.length; i++) {
            let table_head_cell = document.createElement('th');
            table_head_cell.innerHTML = `${capatalize(this.headers[i])} : ${this.types[i]}`;
            table_head_row.appendChild(table_head_cell);
        }
        table_body.appendChild(table_head_row);

        /* Add New */
        let table_add_row = document.createElement('tr');
        for (let i = 0; i < this.headers.length; i++) {
            let table_add_cell = document.createElement('td');
            let table_cell_type = this.types[i];
            let input = null;

            switch (table_cell_type) {
                case 'int':
                    input = document.createElement('input');
                    input.setAttribute('type', 'number');
                    input.classList.add('add_row_data');
                    input.setAttribute('column', this.headers[i]);
                    break;
                
                case 'str':
                    input = document.createElement('input');
                    input.setAttribute('type', 'text');
                    input.classList.add('add_row_data');
                    input.setAttribute('column', this.headers[i]);
                    break;
                
                case 'bool':
                    input = document.createElement('input');
                    input.setAttribute('type', 'checkbox');
                    input.classList.add('add_row_data');
                    input.setAttribute('column', this.headers[i]);
                    break;
                
                case 'date':
                    input = document.createElement('input');
                    input.setAttribute('type', 'date');
                    input.classList.add('add_row_data');
                    input.setAttribute('column', this.headers[i]);
                    break;
                
                case 'datetime':
                    input = document.createElement('input');
                    input.setAttribute('type', 'datetime-local');
                    input.classList.add('add_row_data');
                    input.setAttribute('column', this.headers[i]);
                    break;
                
                case 'float':
                    input = document.createElement('input');
                    input.setAttribute('type', 'number');
                    input.classList.add('add_row_data');
                    input.setAttribute('column', this.headers[i]);
                    break;
                
                case 'id':
                    input = document.createElement('input');
                    input.setAttribute('type', 'submit');
                    input.setAttribute('value', 'Add');
                    input.classList.add('add_row_submit');
                    input.addEventListener('click', (e) => {
                        e.preventDefault();
                        this.addNewRow();
                    });
                    break;
                
                default:
                    input_type = 'text';
                    break;
            }
            
            table_add_cell.appendChild(input);

            table_add_row.appendChild(table_add_cell);
        }
        table_body.appendChild(table_add_row);

        /* Table Data */
        for (let row=0; row<this.data.length; row++) {
            let table_body_row = document.createElement('tr');
            let row_id = this.data[row][0];

            for (let col=0; col<this.headers.length; col++) {
                let table_body_cell = document.createElement('td');
                
                let cell_name = this.headers[col];
                let cell_type = this.types[col];
                let cell_value = this.data[row][col];

                table_body_cell.innerHTML = cell_value;
                table_body_cell.setAttribute('data-id', row_id);
                table_body_cell.setAttribute('data-type', cell_type);
                table_body_cell.setAttribute('data-key', cell_name);
                table_body_cell.setAttribute('data-value', cell_value);

                if (cell_name != 'id') {
                    table_body_cell.addEventListener('dblclick', (e) => {
                        if (!this.inEditing(e.target)) {
                            this.startEditing(e.target);
                        }
                    })  
                }
                

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

    get_types() {
        return this.types;
    }

    get_data() {
        return this.data;
    }

    startEditing(td) {
        let current_editing = this.findEditing();
        if (current_editing) {
            this.cancelEditing(current_editing);
        }

        td.classList.add('editing');
        this.createEditingToolbar(td);

        let input = td.querySelector('.toolbar-input');
        input.focus();
    }

    cancelEditing(td) {
        td.innerHTML = td.getAttribute('data-value');
        td.classList.remove('editing');
        //this.removeToolbar();
    }

    clickOff() {

    }

    finishEditing(td) {
        td.classList.remove('editing');

        let input = td.querySelector('input');
        let new_value = null;
        if (input.getAttribute('type') == 'checkbox') {
            if (input.checked) {
                new_value = 1;
            }
            else {
                new_value = 0;  
            }
        } else {
            new_value = input.value;
        }

        this.sendData(td, new_value);
    
        td.innerHTML = '';
        td.innerHTML = new_value;
    }

    inEditing(td) {
        return td.classList.contains('editing');
    }

    createEditingToolbar(td) {
        const save_btn = document.createElement('button');
        const cancel_btn = document.createElement('button');
        const data_type = td.getAttribute('data-type');
        let input_type = null;
        switch (data_type){
            case 'int':
                input_type = 'number';
                break;
            case 'str':
                input_type = 'text';
                break;
            case 'bool':
                input_type = 'checkbox';
                break;
            case 'date':
                input_type = 'date';
                break;
            case 'datetime':
                input_type = 'datetime-local';
                break;
            case 'float':
                input_type = 'number';
                break;
            default:
                input_type = 'text';
                break;

        }
        const input = document.createElement('input');
        input.setAttribute('type', input_type);
        if (input_type == 'checkbox') {
            if (td.getAttribute('data-value') != '0') {
                input.checked = true;
            }
            else {
                input.checked = false;
            }
        }
        else {
            input.setAttribute('value', td.getAttribute('data-value'));
        }
        input.classList.add('toolbar-input');
        const toolbar = document.createElement('div');

        save_btn.classList.add('save_btn');
        cancel_btn.classList.add('cancel_btn');
        toolbar.classList.add('toolbar');
        
        save_btn.textContent = 'Save';
        cancel_btn.textContent = 'Cancel';

        toolbar.appendChild(input);
        toolbar.appendChild(cancel_btn);
        toolbar.appendChild(save_btn);

        td.innerHTML = '';
        td.appendChild(toolbar);

        save_btn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.finishEditing(td);
        });

        cancel_btn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.cancelEditing(td);
        });

        input.addEventListener('keydown', (e) => {
            if (e.key == 'Enter') {
                this.finishEditing(td);
            }
            else if (e.key == 'Escape') {
                this.cancelEditing(td);
            }
        });
    }

    findEditing() {
        let table_body = this.table.childNodes[0];
        let rows = table_body.childNodes;

        for (let row=0; row<rows.length; row++) {
            let cells = rows[row].childNodes;
            for (let col=0; col<cells.length; col++) {
                if (cells[col].classList.contains('editing')) {
                    return cells[col];
                }
            }
        }
        return null;

    }

    sendData(td, new_value) {
        let row_id = td.getAttribute('data-id');
        let cell_name = td.getAttribute('data-key');
        let cell_type = td.getAttribute('data-type');

        let current_value = td.getAttribute('data-value');
        
        if (new_value == current_value) {
            return;
        }

        $.ajax({
            headers: { "X-CSRFToken": csrf_token },
            url: `/api/update/${this.table_name}/${row_id}/${cell_name}/${cell_type}/${new_value}/`,
            type: 'POST',
            success: function(response) {
                console.log(response);

                // When the server does not respond with a valid response
                // -> reset the cell to its previous value
                if (response.hasOwnProperty('new_value')) {
                    td.setAttribute('data-value', response['new_value']);
                } else {
                    td.innerHTML = td.getAttribute('data-value');
                }
            }
        })
    }

    addNewRow() {
        let arr_row_inputs = document.querySelectorAll('.add_row_data');

        console.log(arr_row_inputs);

        let data = {};
        for (let i = 0; i < arr_row_inputs.length; i++) {
            let input = arr_row_inputs[i];
            let column = input.getAttribute('column');
            let input_value = null

            if (input.type == 'checkbox') {
                if (input.checked) {
                    input_value = 1;
                }
                else {
                    input_value = 0;
                }
            } else {
                input_value = input.value;
            }

            data[column] = input_value;
        }

        $.ajax({
            headers: { "X-CSRFToken": csrf_token },
            url: `/api/add/${this.table_name}/`,
            type: 'POST',
            data: data,
            success: function(response) {
                console.log(response);
            }
        })

        for (let i = 0; i < arr_row_inputs.length; i++) {
            let input = arr_row_inputs[i];
            
            if (input.type == 'checkbox') {
                input.checked = false;
            } else {
                input.value = "";
            }
        }

        // TODO: Get data of table again
        this.draw_table_view();
    }
}