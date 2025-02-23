export const CONTAINER = {
    title: "Container",
    description: "A simple div container that can hold one nested component.",
    prefix: "container",
    style: "",
    isContainer: true,
    defaultStyling: {
        minHeight: '5vh',
        minWidth: '5vw',
        border: "1px solid gray",
        padding: "10px"
    },
    getContent: () => {
        const id = Components.getUniqueId(CONTAINER);
        const div = Components.createDiv();
        div.id = id;
        div.ondragover = Components.onDragOver();
        div.ondrop = Components.onDrop(id);
        return div;
    },
    getSettingsForm: (component) => {
        const form = Components.createDefaultSettingsForm(component, CONTAINER.title);
        return form;
    }
};

export const GRID = {
    title: "Grid",
    description: "A grid with customizable rows and columns.",
    prefix: "grid",
    style: "",
    isContainer: false,
    defaultStyling: {
        width: "100%",  // Ensure grid fills the width of its container
        height: "100%", // Ensure grid fills the height of its container
        border: "1px solid green",
        padding: "10px",
    },
    getContent: () => {
        const id = Components.getUniqueId(GRID);
        const table = document.createElement('table');
        table.id = id;
        table.dataset.rows = 2;
        table.dataset.cols = 2;

        // Create grid with default 2 rows and 2 columns
        Components.createGrid(table, 2, 2);

        // Set the default styling for the table
        for (let [key, value] of Object.entries(GRID.defaultStyling)) {
            table.style[key] = value;
        }

        return table;
    },
    getSettingsForm: (component) => {
        const form = Components.createDefaultSettingsForm(component, GRID.title);
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
    defaultStyling: {
        fontSize: "24px",
        fontWeight: "bold",
        color: "black"
    },
    getContent: () => {
        const h1 = document.createElement('h1');
        h1.textContent = "Default Title";
        h1.content = "Default Title";
        return h1;
    },
    getSettingsForm: (component) => {
        const form = Components.createDefaultSettingsForm(component, TITLE.title);
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
    defaultStyling: {
        fontSize: "16px",
        padding: "5px",
        color: "black"
    },
    getContent: () => {
        const p = document.createElement('p');
        p.textContent = "Default paragraph text...";
        return p;
    },
    getSettingsForm: (component) => {
        const form = Components.createDefaultSettingsForm(component, TEXT.title);
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
    defaultStyling: {
        listStyleType: "disc",
        padding: "10px"
    },
    getContent: () => {
        const id = Components.getUniqueId(LIST);
        const ul = document.createElement('ul');
        ul.id = id;
        const addItemLi = document.createElement('li');
        ul.appendChild(addItemLi);
        const addItemDiv = Components.createDiv();
        addItemDiv.style.textAlign = 'center';
        addItemLi.appendChild(addItemDiv);
        addItemDiv.textContent = "+";
        addItemDiv.onclick = (event) => {
            const newId = Components.getUniqueId(LIST);
            const newLi = document.createElement('li');
            const lastChild = ul.lastElementChild;
            newLi.id = newId;
            ul.insertBefore(newLi, lastChild);
            Editor.getInstance().addComponent(newId, CONTAINER);
        };
        ul.style.listStyleType = 'disc';
        return ul;
    },
    getSettingsForm: (component) => {
        const form = Components.createDefaultSettingsForm(component, LIST.title);
        const dotToggle = Components.createCheckbox("Hide bullet points", false, (checked) => {
            component.style.listStyleType = checked ? 'none' : 'disc';
            if (checked) {
                component.classList.add('unlisted');
                component.style.listStyleType = 'none';
            } else {
                component.classList.remove('unlisted');
                component.style.listStyleType = 'disc';
            }
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
    defaultStyling: {
        color: "blue",
        textDecoration: "underline"
    },
    getContent: () => {
        const a = document.createElement('a');
        a.href = "#";
        a.textContent = "Click here";
        return a;
    },
    getSettingsForm: (component) => {
        const form = Components.createDefaultSettingsForm(component, LINK.title);
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
    defaultStyling: {
        maxWidth: "100%",
        height: "auto"
    },
    getContent: () => {
        const img = document.createElement('img');
        img.src = "https://via.placeholder.com/150";
        img.alt = "Placeholder Image";
        img.style.cssText = "max-width: 100%; height: auto;";
        return img;
    },
    getSettingsForm: (component) => {
        const form = Components.createDefaultSettingsForm(component, IMAGE.title);
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
                const inner = document.createElement('div');
                inner.dataset.type = CONTAINER.prefix;
                Components.addDefaultStyling(inner, CONTAINER.defaultStyling);
                inner.ondragover = Components.onDragOver();
                inner.ondrop = Components.onDrop(id);
                inner.id = id;

                td.appendChild(inner);

                tr.appendChild(td);
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

    static onClickRemoveComponents(id) {
        return () => {
            const deletionTargets = Components.getElementsById(id);
            console.log('deletionTargets', deletionTargets);
            deletionTargets.forEach(t => t.remove());
        }
    }

    static createButton(text) {
        const button = document.createElement('button');
        button.innerText = text;
        return button;
    }

    static getElementsByLinkedId(id) {
        return document.querySelectorAll(`[data-linked-id="${id}"]`);
    }

    static getElementsById(id) {
        const list = this.getElementsByLinkedId(id);
        const owningComponent = document.getElementById(id);

        return [...list, ...(owningComponent ? [owningComponent] : [])];
    }

    static createDefaultSettingsForm(component, title) {
        const form = document.createElement('form');

        // Create a label and textarea for multiline CSS input
        const label = document.createElement('label');
        label.textContent = `Custom Styles (${title}):`;
        label.style.display = 'block';
        label.style.marginBottom = '8px';

        const textarea = document.createElement('textarea');
        textarea.rows = 10;
        textarea.cols = 40;
        textarea.style.width = '100%';
        textarea.style.resize = 'vertical';
        textarea.placeholder = 'width: 100%;\nheight: 300px;\nbackground-color: lightgray;';

        // Convert single-line CSS to multiline format
        const cssText = component.getAttribute('style') || '';
        textarea.value = cssText
            .split(';')
            .filter(Boolean)
            .map(rule => rule.trim() + ';')
            .join('\n');

        // Apply styles to the component when textarea content changes
        textarea.addEventListener('input', () => {
            try {
                const css = textarea.value
                    .split('\n')
                    .map(line => line.trim())
                    .filter(Boolean)
                    .join(' ');
                component.style.cssText = css;
            } catch (error) {
                console.error('Invalid CSS:', error);
            }
        });

        // Append everything to the form
        form.appendChild(label);
        form.appendChild(textarea);

        return form;
    };


    static addDefaultStyling(component, defaultStyling) {
        if (component && defaultStyling) {
            for (let property in defaultStyling) {
                component.style[property] = defaultStyling[property];
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

    getSubmissionWindow() {
        const submissionWindow = document.getElementById('editor-submit-dialog');
        if (submissionWindow) {
            return submissionWindow;
        }
    }

    onClickSubmitEvent() {
        return () => {
            this.hideSubmissionWindow(false);
        }
    }

    onClickHideEvent() {
        return () => {
            this.hideSubmissionWindow(true);
        }
    }

   onClickUpdateSubmitDescription(component) {
        return () => {
            const content = this.getContent();
            component.innerText = this.getContent().innerHTML;
        }
    }

    hideSubmissionWindow(hide) {
        console.log(hide);
        if (hide) {
            this.getSubmissionWindow().classList.add('hidden');
        } else {
            this.getSubmissionWindow().classList.remove('hidden');
        }
    }

    getContent() {
        const content = document.getElementById('content');
        if (content) return content;
        Toast.error("Could not get content. Exiting ..");
    }

    addComponent(targetId, component) {
        console.log('adding component: ', targetId, component);
        const {title, description, prefix, style, isContainer, getSettingsForm, getContent, defaultStyling} = component;
        const generatedComponent = getContent();
        generatedComponent.dataset.type = component.prefix;
        generatedComponent.id = generatedComponent.id ? generatedComponent.id : Components.getUniqueId(component);
        Components.addDefaultStyling(generatedComponent, defaultStyling);
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
        li.dataset.linkedId = generatedComponent.id;
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
        const deleteButton = Components.createButton("x");

        deleteButton.onclick = Components.onClickRemoveComponents(id);

        inner.appendChild(deleteButton);

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