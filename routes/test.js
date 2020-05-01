const express = require("express");
const asynchandler = require('../utils/asynchandler');
const HttpError = require("../models/httperror")
const router = express.Router();

router.use(express.json());

router.get('/echo', (req, res) => {
    res.send(req.rawHeaders);
});

router.post('/echo', (req, res) => {
    res.send(req.body);
});

router.get('/temp', (req, res) => {
    const User = require("../models/user");
    console.log(new User.Builder());
});

router.get('/dbtest', asynchandler(async (req, res) => {
    const collection = req.app.locals.db.collection('tesy');
    const r = await collection.find({});
    console.log('go');
    throw new Error("test");
    console.log(r);
    res.send(r.value);
}));

router.get('/error1', (req, res, next) => {
    next(new Error("wtf"));
});

router.get('/error2', (req, res, next) => {
    next(new HttpError(400, "hell"));
});

module.exports = router;
