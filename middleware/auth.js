const Session = require('../models/session');

const accessTokenHeader = 'x-access-token';

module.exports = async function (req, res, next) {
    const token = req.get(accessTokenHeader);
    const session = await Session.findByToken(token);
    if (session && !session.errors)
        req.session = session;
    next();
};
