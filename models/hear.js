// 글

const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const hearSchema = new Schema({
    userId: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    content: String,
    createdAt: Date
}, {
    timestamps: {
        createdAt: 'createdAt'
    }
});

const Hear = mongoose.model('Hear', hearSchema);

module.exports = Hear;