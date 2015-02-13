/**
 * Created by po0ya on 30/12/14.
 */

findRoots = function (dictionary) {
    var roots = [];
    for (nd in dictionary) {
        if (dictionary[nd].parent == null) {
            roots.push({label: dictionary[nd].name});
        }
    }
    return roots;
};

var sampleData = [
    {
        name: "root",
        parent: null
    },
    {
        name: "esm",
        parent: "root"
    }
];

$(function() {
    var modifiedObject = findRoots(sampleData);
    console.log(modifiedObject);
    return modifiedObject;
});

