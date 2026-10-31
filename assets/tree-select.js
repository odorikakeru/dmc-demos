var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

dmcfuncs.treeOverflow = function (count) {
  return "+" + count + " more";
};

dmcfuncs.treeFilter = function (query, node) {
  var text = query.trim().toLowerCase();
  return String(node.label).toLowerCase().startsWith(text) ||
    node.value.toLowerCase().startsWith(text);
};

dmcfuncs.treeNode = function (payload) {
  return React.createElement(
    "span",
    {className: "tree-custom-node"},
    payload.node.label,
    payload.hasChildren
      ? React.createElement(
          "span",
          {className: "tree-node-count"},
          payload.node.children.length + " items"
        )
      : null
  );
};

dmcfuncs.treePill = function (payload) {
  return React.createElement(
    "span",
    {className: "tree-custom-pill"},
    payload.node.label,
    React.createElement(
      "button",
      {
        type: "button",
        "aria-label": "Remove " + payload.node.label,
        disabled: payload.disabled,
        onMouseDown: function (event) { event.preventDefault(); },
        onClick: function (event) {
          event.stopPropagation();
          payload.onRemove();
        }
      },
      "x"
    )
  );
};
