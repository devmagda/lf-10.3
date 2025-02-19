export const CONTAINER = {
    title: "Container",
    description: "A simple div container that can hold one nested component.",
    prefix: "container",
    style: "",
    isContainer: true,
    getContent: () => {
        const id = Components.getUniqueId(CONTAINER);
        const div = Components.createDiv();
        div.id = id;
        div.ondragover = Components.onDragOver();
        div.ondrop = Components.onDrop(id);
        return div;
    },
    getSettingsForm: () => {
        const form = document.createElement('form');
        form.innerHTML = "<p>No settings for Container.</p>";
        return form;
    }
};

export const GRID = {
    title: "Grid",
    description: "A grid with customizable rows and columns.",
    prefix: "grid",
    style: "",
    isContainer: false,
    getContent: () => {
        const id = Components.getUniqueId(GRID);
        const table = document.createElement('table');
        table.id = id;
        table.dataset.rows = 2;
        table.dataset.cols = 2;
        Components.createGrid(table, 2, 2);
        return table;
    },
    getSettingsForm: (component) => {
        const form = document.createElement('form');
        const rowsInput = Components.createInput("Rows:", component.dataset.rows, "number", (val) => {
            component.dataset.rows = val;
            Components.createGrid(component, parseInt(val), parseInt(component.dataset.cols));
        });
        const colsInput = Components.createInput("Columns:", component.dataset.cols, "number", (val) => {
            component.dataset.cols = val;
            Components.createGrid(component, parseInt(component.dataset.rows), parseInt(val));
        });
        form.append(rowsInput, colsInput);
        return form;
    }
};

export const TITLE = {
    title: "Title",
    description: "A header element (h1) with customizable text.",
    prefix: "title",
    style: "font-size: 24px; font-weight: bold;",
    isContainer: false,
    getContent: () => {
        const h1 = document.createElement('h1');
        h1.textContent = "Default Title";
        h1.content = "Default Title";
        return h1;
    },
    getSettingsForm: (component) => {
        const form = document.createElement('form');
        const input = Components.createInput("Title Text:", component.textContent, "text", (val) => {
            component.textContent = val;
        });
        form.appendChild(input);
        return form;
    }
};

export const TEXT = {
    title: "Text",
    description: "A multiline text paragraph.",
    prefix: "text",
    style: "font-size: 16px; padding: 5px;",
    isContainer: false,
    getContent: () => {
        const p = document.createElement('p');
        p.textContent = "Default paragraph text...";
        return p;
    },
    getSettingsForm: (component) => {
        const form = document.createElement('form');
        const textarea = Components.createTextarea("Paragraph Text:", component.textContent, (val) => {
            component.innerHTML = val.replace(/\n/g, '<br>');
        });
        form.appendChild(textarea);
        return form;
    }
};

export const LIST = {
    title: "List",
    description: "An unordered list with customizable items and dot visibility.",
    prefix: "list",
    style: "",
    isContainer: false,
    getContent: () => {
        const ul = document.createElement('ul');
        ul.style.listStyleType = 'disc';
        ["Item 1", "Item 2", "Item 3"].forEach((text) => {
            const li = document.createElement('li');
            li.textContent = text;
            ul.appendChild(li);
        });
        return ul;
    },
    getSettingsForm: (component) => {
        const form = document.createElement('form');
        const dotToggle = Components.createCheckbox("Hide bullet points", false, (checked) => {
            component.style.listStyleType = checked ? 'none' : 'disc';
        });
        form.appendChild(dotToggle);
        return form;
    }
};

export const LINK = {
    title: "Link",
    description: "A clickable link with customizable text and URL.",
    prefix: "link",
    style: "color: blue; text-decoration: underline;",
    isContainer: false,
    getContent: () => {
        const a = document.createElement('a');
        a.href = "#";
        a.textContent = "Click here";
        return a;
    },
    getSettingsForm: (component) => {
        const form = document.createElement('form');
        const titleInput = Components.createInput("Link Text:", component.textContent, "text", (val) => {
            component.textContent = val;
        });
        const urlInput = Components.createInput("URL:", component.href, "text", (val) => {
            component.href = val;
        });
        form.append(titleInput, urlInput);
        return form;
    }
};

export const IMAGE = {
    title: "Image",
    description: "An image component with customizable URL.",
    prefix: "image",
    style: "max-width: 100%; height: auto;",
    isContainer: false,
    getContent: () => {
        const img = document.createElement('img');
        img.src = "https://via.placeholder.com/150";
        img.alt = "Placeholder Image";
        img.style.cssText = "max-width: 100%; height: auto;";
        return img;
    },
    getSettingsForm: (component) => {
        const form = document.createElement('form');
        const urlInput = Components.createInput("Image URL:", component.src, "text", (val) => {
            component.src = val;
        });
        form.appendChild(urlInput);
        return form;
    }
};

class Components {
    static #componentsMap = null;

    static getComponentsMap() {
        if (!this.#componentsMap) {
            this.#componentsMap = new Map([
                ["container", CONTAINER],
                ["grid", GRID],
                ["title", TITLE],
                ["text", TEXT],
                ["list", LIST],
                ["link", LINK],
                ["image", IMAGE]
            ]);
        }
        return this.#componentsMap;
    }

    static getComponents() {
        return Array.from(this.getComponentsMap().values());
    }

    static getComponentByPrefix(prefix) {
        return this.getComponentsMap().get(prefix);
    }

    static getFromEvent(event) {
        // Retrieve the dropped JSON data
        const componentDataString = event.dataTransfer.getData('application/json');

        if (componentDataString) {
            // Parse the JSON string back into an object
            return JSON.parse(componentDataString);
        }
        return null;  // If no data is found, return null
    }

    static createInput(labelText, value, type = "text", onChange = () => {
    }) {
        const label = document.createElement('label');
        label.textContent = labelText;
        const input = document.createElement('input');
        input.type = type;
        input.value = value;
        input.addEventListener('input', (e) => onChange(e.target.value));
        label.appendChild(input);
        return label;
    }

    static createTextarea(labelText, value, onChange = () => {
    }) {
        const label = document.createElement('label');
        label.textContent = labelText;
        const textarea = document.createElement('textarea');
        textarea.value = value;
        textarea.addEventListener('input', (e) => onChange(e.target.value));
        label.appendChild(textarea);
        return label;
    }

    static createCheckbox(labelText, checked, onChange = () => {
    }) {
        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = checked;
        checkbox.addEventListener('change', (e) => onChange(e.target.checked));
        label.appendChild(checkbox);
        label.append(labelText);
        return label;
    }

    static clearElement(element) {
        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }
    }

    static createGrid(table, rows, cols) {
        table.innerHTML = "";
        for (let i = 0; i < rows; i++) {
            const tr = document.createElement('tr');
            for (let j = 0; j < cols; j++) {
                const td = document.createElement('td');
                const id = Components.getUniqueId(GRID) + "_td";
                td.id = id;
                td.appendChild(CONTAINER.getContent());

                tr.appendChild(td);

                td.ondragover = Components.onDragOver();
                td.ondrop = Components.onDrop(id);
            }
            table.appendChild(tr);
        }
    }

    static createListItem(title, id) {
        const template = document.createElement('li');
        template.dataset.linkedId = id;
        const inner = document.createElement('div');
        inner.classList.add('component-list-entry');
        const innerText = document.createElement('span');

        innerText.innerText = title;


        inner.appendChild(innerText);
        template.appendChild(inner);

        return {template, inner, innerText};
    }

    static getUniqueId(component) {
        const {prefix} = component;
        const salt = Date.now() * Math.random();
        return prefix + '_' + salt.toString(16).substring(4);
    }

    static createDiv() {
        const div = document.createElement('div');
        div.classList.add('component-container')
        //div.dataset.allowContainer = true; welp
        return div;
    }

    static onDragOver() {
        return (event) => {
            event.preventDefault();
            event.stopPropagation();
        }
    }

    static onDrop(id) {
        return (event) => {
            event.stopPropagation();
            const componentTemplate = Components.getFromEvent(event);

            if (componentTemplate) {
                const component = Components.getComponentByPrefix(componentTemplate.prefix);
                if (component) {
                    Editor.getInstance().addComponent(id, component);
                }
            } else {
                Toast.error("Could not create Component. Please see logs for details!");
                console.log("EVENT: ", event);
            }
        }
    }
}

export class Editor {
    static #instance;

    constructor() {
        if (Editor.#instance) {
            return Editor.#instance; // Return existing instance if already created
        }

        this.toolbarDiv = document.getElementById('toolbar');
        this.contentDiv = document.getElementById('content');
        this.settingsDiv = document.getElementById('settings');

        const valid = (this.toolbarDiv && this.contentDiv && this.settingsDiv);
        if (!valid) {
            Toast.error("Could not open editor ..");
        }

        Components.getComponents().forEach(c => this.addComponentTemplate(c));
        this.addComponent('content', CONTAINER);

        Editor.#instance = this; // Store the instance
    }

    static getInstance() {
        if (!Editor.#instance) {
            Editor.#instance = new Editor();
        }
        return Editor.#instance;
    }

    getComponentTemplateList() {
        const templateList = document.getElementById('component-template-list');
        if (templateList) return templateList;
        Toast.error("Could not get template list. Exiting ..");
    }

    getContent() {
        const content = document.getElementById('content');
        if (content) return content;
        Toast.error("Could not get content. Exiting ..");
    }

    addComponent(targetId, component) {
        console.log('adding component: ', targetId, component);
        const {title, description, prefix, style, isContainer, getSettingsForm, getContent} = component;
        const generatedComponent = getContent();
        generatedComponent.style = style;
        if (!generatedComponent.id) {
            generatedComponent.id = Components.getUniqueId(component);
        }
        const target = document.getElementById(targetId);
        if (target) {
            target.appendChild(generatedComponent);
            this.addComponentList(generatedComponent.id, component);
            this.addSetting(generatedComponent, component);
        } else {
            Toast.error("Could not get target or componentList for targetId " + targetId);
            console.log("this one..");
        }
    }

    getSettings() {
        const settings = document.getElementById('settings-list');
        if (settings) return settings;
        Toast.error("Could not get settings. Exiting ..");
    }

    addSetting(generatedComponent, component) {
        const {title, description, prefix, style, isContainer, getSettingsForm, getContent} = component;
        const li = document.createElement('li');
        li.appendChild(getSettingsForm(generatedComponent));
        this.getSettings().appendChild(li);
    }

    addComponentTemplate(component) {
        const {title, prefix} = component;
        const {template} = Components.createListItem(title);
        template.draggable = true;
        template.ondragstart = (event) => {
            event.dataTransfer.setData('application/json', JSON.stringify(component));
        };
        template.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', prefix);
        });
        this.getComponentTemplateList().appendChild(template);
    }

    addComponentList(id, component) {
        const {title} = component;
        const {template, inner} = Components.createListItem(title, id);
        inner.style.display = 'flex';
        template.idLink = id;
        this.getComponentList().appendChild(template);
    }

    getComponentList() {
        const componentList = document.getElementById('component-list');
        if (componentList) return componentList;
        Toast.error("Could not get component list. Exiting ..");
    }

    removeComponent(targetId) {
        const targetParent = document.getElementById(targetId)?.parentElement;
        if (targetParent) {
            Components.clearElement(targetParent);
        } else {
            Toast.error("Could not remove component with id " + targetId);
        }
    }
}

export class Toast {
    static info(text) {
        Toastify({
            text,
            duration: 3000,
            destination: "https://github.com/apvarun/toastify-js",
            newWindow: true,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "left", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
                background: "var(--success)",
            },
            onClick: function () {
            } // Callback after click
        }).showToast();
    }

    static warn(text) {
        Toastify({
            text,
            duration: 3000,
            gravity: "bottom", // `top` or `bottom`
            position: "right", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
                background: "var(--warning)",
            },
            onClick: function () {
            } // Callback after click
        }).showToast();
    }

    static error(text) {
        Toastify({
            text,
            duration: 3000,
            destination: "https://github.com/apvarun/toastify-js",
            newWindow: true,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "left", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
                background: "var(--error)",
            },
            onClick: function () {
            } // Callback after click
        }).showToast();
    }
}


export default Editor;