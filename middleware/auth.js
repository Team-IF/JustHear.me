const express = require("express");
const Session = require('../models/session');

const accessTokenHeader = 'x-access-token';

module.exports = async function (req, res) {
    const token = req.get(accessTokenHeader);

    const db = req.app.locals.db;
    const sessionCollection = db.collection('sessions');
    const session = await sessionCollection.findOne({ accessToken: token });

    if (session)
        req.session = new Session(session.uuid, session.accessToken, session.expireDate);
};
