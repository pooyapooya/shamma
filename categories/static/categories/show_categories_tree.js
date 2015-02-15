// ITNOG

findChildrens = function (dictionary, parent) {
    var roots = [];
    for (var nd in dictionary) {
        if (dictionary[nd].parent == parent) {
            childrens = findChildrens(dictionary, dictionary[nd].id);
            roots.push({
                label: dictionary[nd].name,
                id: dictionary[nd].id,
                children: childrens
            });
        }
    }
    return roots;
};

makeCorrect = function (data) {
    var correct = findChildrens(data, null);
    return correct;
};

makeTree = function () {

    $.getJSON('/categories/get_data/', function (data) {
        console.log(data);
        var treeData = makeCorrect(data);
        $('#tree1').tree({
            data: treeData
        });
    });
};

reloadTree = function () {

    $.getJSON('/categories/get_data/', function (data) {
        console.log(data);
        var treeData = makeCorrect(data);
//        $('#tree1').tree({
//            data: treeData
//        });
        $('#tree1').tree('loadData', treeData);
    });
};

$(function () {
    makeTree();
    
    $('#tree1').bind(
        'tree.click',
        function (event) {
            // The clicked node is 'event.node'
            var node = event.node;
            window.location = '/categories/' + node.id;
        }
    );
});
