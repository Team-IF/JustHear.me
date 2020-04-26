const express = require("express");
const router = express.Router();
let db;

router.use(express.json());

router.get('/echo', (req, res) => {
    res.send(req.rawHeaders);
});

router.post('/echo', (req, res) => {
    res.send(req.body);
});

router.get('/dbtest', async (req, res) => {
    const collection = db.collection('tesy');
    const r = await collection.find({});
    console.log(r);
    res.send(r.value);
});

module.exports = function (s) {
    db = s;
    return router;
};
