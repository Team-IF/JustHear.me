const express = require('express');
const router = express.Router();

router.use(express.json());

router.get('/echo', (req, res) => {
    res.send(req.rawHeaders);
});

module.exports = router;
