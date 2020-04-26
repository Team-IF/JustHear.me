const express = require("express");
const router = express.Router();

router.use(express.json());

router.get('/echo', (req, res) => {
    res.send(req.rawHeaders);
});

router.post('/echo', (req, res) => {
    res.send(req.body);
});

module.exports = router;