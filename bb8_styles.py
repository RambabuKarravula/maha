# BB8 theme toggle styles
bb8_css = """
<style>
/* BB8 Toggle Base */
.bb8-toggle {
    --toggle-size: 16px;
    --toggle-width: 10.625em;
    --toggle-height: 5.625em;
    --toggle-offset: calc((var(--toggle-height) - var(--bb8-diameter)) / 2);
    --toggle-bg: linear-gradient(#2c4770, #070e2b 35%, #628cac 50% 70%, #a6c5d4) no-repeat;
    --bb8-diameter: 4.375em;
    --radius: 99em;
    --transition: 0.4s;
    --accent: #de7d2f;
    --bb8-bg: #fff;
    cursor: pointer;
    font-size: var(--toggle-size);
}

/* BB8 Checkbox */
.bb8-toggle__checkbox {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    display: none;
}

/* Toggle Container */
.bb8-toggle__container {
    width: var(--toggle-width);
    height: var(--toggle-height);
    background: var(--toggle-bg);
    background-size: 100% 11.25em;
    background-position-y: -5.625em;
    border-radius: var(--radius);
    position: relative;
    transition: var(--transition);
}

/* BB8 Robot */
.bb8 {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: absolute;
    top: calc(var(--toggle-offset) - 1.688em + 0.188em);
    left: var(--toggle-offset);
    transition: var(--transition);
    z-index: 2;
}

/* BB8 Head Container */
.bb8__head-container {
    position: relative;
    transition: var(--transition);
    z-index: 2;
    transform-origin: 1.25em 3.75em;
}

/* BB8 Head */
.bb8__head {
    overflow: hidden;
    margin-bottom: -0.188em;
    width: 2.5em;
    height: 1.688em;
    background: linear-gradient(
        transparent 0.063em,
        dimgray 0.063em 0.313em,
        transparent 0.313em 0.375em,
        var(--accent) 0.375em 0.5em,
        transparent 0.5em 1.313em,
        silver 1.313em 1.438em,
        transparent 1.438em
    ),
    linear-gradient(
        45deg,
        transparent 0.188em,
        var(--bb8-bg) 0.188em 1.25em,
        transparent 1.25em
    ),
    linear-gradient(
        -45deg,
        transparent 0.188em,
        var(--bb8-bg) 0.188em 1.25em,
        transparent 1.25em
    ),
    linear-gradient(var(--bb8-bg) 1.25em, transparent 1.25em);
    border-radius: var(--radius) var(--radius) 0 0;
    position: relative;
    z-index: 1;
    filter: drop-shadow(0 0.063em 0.125em gray);
}

/* BB8 Body */
.bb8__body {
    width: 4.375em;
    height: 4.375em;
    background: var(--bb8-bg);
    border-radius: var(--radius);
    position: relative;
    overflow: hidden;
    transition: var(--transition);
    z-index: 1;
    transform: rotate(45deg);
}

/* BB8 Body Pattern */
.bb8__body::before {
    content: "";
    width: 2.625em;
    height: 2.625em;
    position: absolute;
    border-radius: 50%;
    z-index: 0.1;
    overflow: hidden;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border: 0.313em solid var(--accent);
}

/* BB8 Shadow */
.bb8__shadow {
    content: "";
    width: var(--bb8-diameter);
    height: 20%;
    border-radius: 50%;
    background: #3a271c;
    box-shadow: 0.313em 0 3.125em #3a271c;
    opacity: 0.25;
    position: absolute;
    bottom: 0;
    left: calc(var(--toggle-offset) - 0.938em);
    transition: var(--transition);
    transform: skew(-70deg);
    z-index: 1;
}

/* Toggle Scenery */
.bb8-toggle__scenery {
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    position: relative;
    border-radius: inherit;
}

/* Stars */
.bb8-toggle__star {
    position: absolute;
    width: 0.063em;
    height: 0.063em;
    background: #fff;
    border-radius: var(--radius);
    filter: drop-shadow(0 0 0.063em #fff);
    top: 100%;
}

/* Animations and States */
.bb8-toggle__checkbox:checked + .bb8-toggle__container {
    background-position-y: 0;
}

.bb8-toggle__checkbox:checked + .bb8-toggle__container .bb8 {
    left: calc(100% - var(--bb8-diameter) - var(--toggle-offset));
}

.bb8-toggle__checkbox:checked + .bb8-toggle__container .bb8__body {
    transform: rotate(225deg);
}

.bb8-toggle__checkbox:checked + .bb8-toggle__container .bb8__shadow {
    left: calc(100% - var(--bb8-diameter) - var(--toggle-offset) + 0.938em);
    transform: skew(70deg);
}

/* Hover States */
.bb8-toggle__checkbox:hover + .bb8-toggle__container .bb8__head::before {
    left: 100%;
}

.bb8-toggle__checkbox:checked:hover + .bb8-toggle__container .bb8__head::before {
    left: 0;
}

.bb8:hover .bb8__head::before {
    left: 50% !important;
}
</style>
"""

# BB8 toggle HTML template
bb8_html = """
<div class="theme-toggle">
    <label class="bb8-toggle">
        <input class="bb8-toggle__checkbox" type="checkbox" onclick="toggleTheme()">
        <div class="bb8-toggle__container">
            <div class="bb8-toggle__scenery">
                <div class="bb8-toggle__star"></div>
                <div class="bb8-toggle__star"></div>
                <div class="bb8-toggle__star"></div>
                <div class="bb8-toggle__star"></div>
                <div class="bb8-toggle__star"></div>
                <div class="bb8-toggle__star"></div>
                <div class="bb8-toggle__star"></div>
            </div>
            <div class="bb8">
                <div class="bb8__head-container">
                    <div class="bb8__antenna"></div>
                    <div class="bb8__antenna"></div>
                    <div class="bb8__head"></div>
                </div>
                <div class="bb8__body"></div>
            </div>
            <div class="artificial__hidden">
                <div class="bb8__shadow"></div>
            </div>
        </div>
    </label>
</div>
"""