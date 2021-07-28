import "./scss/main.scss";
import * as sapper from '@sapper/app';

sapper.start({
	target: document.querySelector('#sapper')
});