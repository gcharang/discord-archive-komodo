const {
    resolve
} = require('path')
var {
    staticFileStructure
} = require('./dirStructure.js');
module.exports = {
    name: 'static-file-structure',
    extendPageData($page) {

        $page.staticFileStructure = staticFileStructure
    }
}