const express = require("express");
const Session = require('../models/session');

const accessTokenHeader = 'x-access-token';

module.exports = async function (req, res) {
    const token = req.get(accessTokenHeader);
    const session = await Session.findByToken(token);

    if (session)
        req.session = new Session(session.uuid, session.accessToken, session.expireDate);
};
