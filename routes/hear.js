const express = require('express');
const formidable = require('express-formidable');
const auther = require('../middleware/auth');
const HttpError = require('../models/httperror');
const Hear = require('../models/hear');
const asynchandler = require('../utils/asynchandler');

const router = express.Router();
router.use(formidable());

router.get('/read/:id', asynchandler(async (req, res) => {
    const hear = await Hear.findById(req.params.id).exec();
    if (!hear)
        throw HttpError.NotFound;

    res.send(hear);
}));

router.post('/upload', asynchandler(auther), asynchandler(async (req, res) => {
    if (!req.session || !req.session.checkValidation())
        throw HttpError.Unauthorized;

    const hear = new Hear({
        userId: req.session.userId,
        title: req.fields.title,
        content: req.fields.content
    });
    const savedHear = await hear.save();

    res.send({
        result: true,
        _id: savedHear._id
    });
}));

router.post('/edit/:id', asynchandler(auther), asynchandler(async (req, res) => {
    const hear = await Hear.findById(req.params.id).exec();
    if (!hear)
        throw HttpError.NotFound;

    if (!req.session || !req.session.checkValidation())
        throw HttpError.Unauthorized;

    if (hear.userId !== req.session.userId)
        throw HttpError.Forbidden;

    await hear.updateOne({
        title: req.fields.title,
        content: req.fields.content
    });

    res.send({
        result: true,
        _id: hear._id
    });
}));

module.exports = router;
