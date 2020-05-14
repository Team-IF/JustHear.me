const uuid4 = require('uuid4');

// uuid db optimizing
module.exports = function () {
    const tokens = uuid4().split('-');
    return tokens[2] + tokens[1] + tokens[0] + tokens[3] + tokens[4];
};