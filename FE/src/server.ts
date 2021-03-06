import sirv from 'sirv';
import polka from 'polka';
import compression from 'compression';
import * as sapper from '@sapper/server';

const { PORT, NODE_ENV } = process.env;
const dev = NODE_ENV === 'development';

const { createServer } = require('https');
const { readFileSync } = require('fs');
const ssl_port = 443;

const options = {
	key: readFileSync('./ssl/localhost-key.pem'),
	cert: readFileSync('./ssl/localhost.pem')
};

const { handler } = polka()
	.use(
		compression({ threshold: 0 }),
		sirv('static', { dev }),
		sapper.middleware()
	)
// Mount Polka to HTTPS server
createServer(options, handler).listen(ssl_port, _ => {
    console.log(`> Running on https://localhost:${ssl_port}`);
});