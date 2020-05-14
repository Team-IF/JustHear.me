// 글

const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const hearSchema = new Schema({
    userId: String,
    title: String,
    content: String,
    createdAt: Date
}, {
    timestamps: {
        createdAt: 'createdAt'
    }
});

const Hear = mongoose.model('Hear', hearSchema);

module.exports = Hear;