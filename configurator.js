const fs = require('fs');

function config() {
    if (!process.env.NODE_ENV)
        process.env.NODE_ENV = 'development';
    else
        process.env.NODE_ENV = process.env.NODE_ENV.toLowerCase();
    console.log(`Node Mode: ${process.env.NODE_ENV}`);

    const dotenvPath = `./config/${process.env.NODE_ENV}.env`;

    if (checkFileExists(dotenvPath)) {
        console.log('Configure from ' + dotenvPath);
        const dotenvResult = require('dotenv').config({ path: dotenvPath });

        if (dotenvResult.error) {
            console.log('Dotenv error :');
            console.log(dotenvResult.error);
        }
    }
    else
        console.log('Use Environment Variables');

    return {
        host: process.env.host,
        port: Number(process.env.port),
        dburl: process.env.dburl
    };
}

function checkFileExists(p) {
    try {
        fs.accessSync(p);
        return fs.lstatSync(p).isFile();
    } catch (error) {
        return false;
    }
}

module.exports.config = config;