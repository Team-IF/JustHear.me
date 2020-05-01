module.exports = {
  apps: [{
    name: 'JustHear.me',
    script: 'app.js',

    // Options reference: https://pm2.keymetrics.io/docs/usage/application-declaration/
    exec_mode: 'cluster',
    instances: 1,
    autorestart: true,
    watch: true,
    max_memory_restart: '1G',
    out_file: 'logs/out.log',
    error_file: 'logs/err.log',
    time: true,
    kill_timeout: 2000,
    listen_timeout: 2000,
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    }
  }]
};
