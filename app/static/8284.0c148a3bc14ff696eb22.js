"use strict";(self.webpackChunkUV=self.webpackChunkUV||[]).push([[8284],{8284:(t,o,n)=>{n.r(o),n.d(o,{ion_content:()=>i});var r=n(5873),e=n(636),i=function(){function t(t){(0,r.r)(this,t),this.isScrolling=!1,this.lastScroll=0,this.queued=!1,this.cTop=-1,this.cBottom=-1,this.mode=(0,r.f)(this),this.detail={scrollTop:0,scrollLeft:0,type:"scroll",event:void 0,startX:0,startY:0,startTimeStamp:0,currentX:0,currentY:0,velocityX:0,velocityY:0,deltaX:0,deltaY:0,timeStamp:0,data:void 0,isScrolling:!0},this.fullscreen=!1,this.scrollX=!1,this.scrollY=!0,this.scrollEvents=!1,this.ionScrollStart=(0,r.c)(this,"ionScrollStart",7),this.ionScroll=(0,r.c)(this,"ionScroll",7),this.ionScrollEnd=(0,r.c)(this,"ionScrollEnd",7)}return t.prototype.disconnectedCallback=function(){this.onScrollEnd()},t.prototype.componentDidLoad=function(){this.resize()},t.prototype.onClick=function(t){this.isScrolling&&(t.preventDefault(),t.stopPropagation())},t.prototype.shouldForceOverscroll=function(){var t=this.forceOverscroll,o=this.mode;return void 0===t?"ios"===o&&(0,r.j)("ios"):t},t.prototype.resize=function(){this.fullscreen?(0,r.m)(this.readDimensions.bind(this)):0===this.cTop&&0===this.cBottom||(this.cTop=this.cBottom=0,this.el.forceUpdate())},t.prototype.readDimensions=function(){var t=l(this.el),o=Math.max(this.el.offsetTop,0),n=Math.max(t.offsetHeight-o-this.el.offsetHeight,0);(o!==this.cTop||n!==this.cBottom)&&(this.cTop=o,this.cBottom=n,this.el.forceUpdate())},t.prototype.onScroll=function(t){var o=this,n=Date.now(),e=!this.isScrolling;this.lastScroll=n,e&&this.onScrollStart(),!this.queued&&this.scrollEvents&&(this.queued=!0,(0,r.m)((function(n){o.queued=!1,o.detail.event=t,c(o.detail,o.scrollEl,n,e),o.ionScroll.emit(o.detail)})))},t.prototype.getScrollElement=function(){return Promise.resolve(this.scrollEl)},t.prototype.scrollToTop=function(t){return void 0===t&&(t=0),this.scrollToPoint(void 0,0,t)},t.prototype.scrollToBottom=function(t){void 0===t&&(t=0);var o=this.scrollEl.scrollHeight-this.scrollEl.clientHeight;return this.scrollToPoint(void 0,o,t)},t.prototype.scrollByPoint=function(t,o,n){return this.scrollToPoint(t+this.scrollEl.scrollLeft,o+this.scrollEl.scrollTop,n)},t.prototype.scrollToPoint=function(t,o,n){return void 0===n&&(n=0),r=this,e=void 0,l=function(){var r,e,i,l,c,s,a,u,h;return function(t,o){var n,r,e,i,l={label:0,sent:function(){if(1&e[0])throw e[1];return e[1]},trys:[],ops:[]};return i={next:c(0),throw:c(1),return:c(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function c(i){return function(c){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;l;)try{if(n=1,r&&(e=2&i[0]?r.return:i[0]?r.throw||((e=r.return)&&e.call(r),0):r.next)&&!(e=e.call(r,i[1])).done)return e;switch(r=0,e&&(i=[2&i[0],e.value]),i[0]){case 0:case 1:e=i;break;case 4:return l.label++,{value:i[1],done:!1};case 5:l.label++,r=i[1],i=[0];continue;case 7:i=l.ops.pop(),l.trys.pop();continue;default:if(!((e=(e=l.trys).length>0&&e[e.length-1])||6!==i[0]&&2!==i[0])){l=0;continue}if(3===i[0]&&(!e||i[1]>e[0]&&i[1]<e[3])){l.label=i[1];break}if(6===i[0]&&l.label<e[1]){l.label=e[1],e=i;break}if(e&&l.label<e[2]){l.label=e[2],l.ops.push(i);break}e[2]&&l.ops.pop(),l.trys.pop();continue}i=o.call(t,l)}catch(t){i=[6,t],r=0}finally{n=e=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,c])}}}(this,(function(p){return r=this.scrollEl,n<32?(null!=o&&(r.scrollTop=o),null!=t&&(r.scrollLeft=t),[2]):(i=0,l=new Promise((function(t){return e=t})),c=r.scrollTop,s=r.scrollLeft,a=null!=o?o-c:0,u=null!=t?t-s:0,h=function(t){var o=Math.min(1,(t-i)/n)-1,l=Math.pow(o,3)+1;0!==a&&(r.scrollTop=Math.floor(l*a+c)),0!==u&&(r.scrollLeft=Math.floor(l*u+s)),l<1?requestAnimationFrame(h):e()},requestAnimationFrame((function(t){i=t,h(t)})),[2,l])}))},new((i=void 0)||(i=Promise))((function(t,o){function n(t){try{s(l.next(t))}catch(t){o(t)}}function c(t){try{s(l.throw(t))}catch(t){o(t)}}function s(o){o.done?t(o.value):new i((function(t){t(o.value)})).then(n,c)}s((l=l.apply(r,e||[])).next())}));var r,e,i,l},t.prototype.onScrollStart=function(){var t=this;this.isScrolling=!0,this.ionScrollStart.emit({isScrolling:!0}),this.watchDog&&clearInterval(this.watchDog),this.watchDog=setInterval((function(){t.lastScroll<Date.now()-120&&t.onScrollEnd()}),100)},t.prototype.onScrollEnd=function(){clearInterval(this.watchDog),this.watchDog=null,this.isScrolling&&(this.isScrolling=!1,this.ionScrollEnd.emit({isScrolling:!1}))},t.prototype.render=function(){var t,o=this,n=this.scrollX,i=this.scrollY,l=(0,r.f)(this),c=this.shouldForceOverscroll(),s="ios"===l&&r.i.getBoolean("experimentalTransitionShadow",!0);return this.resize(),(0,r.h)(r.H,{class:Object.assign(Object.assign({},(0,e.c)(this.color)),(t={},t[l]=!0,t["content-sizing"]=(0,e.h)("ion-popover",this.el),t.overscroll=c,t)),style:{"--offset-top":this.cTop+"px","--offset-bottom":this.cBottom+"px"}},(0,r.h)("main",{class:{"inner-scroll":!0,"scroll-x":n,"scroll-y":i,overscroll:(n||i)&&c},ref:function(t){return o.scrollEl=t},onScroll:function(t){return o.onScroll(t)}},(0,r.h)("slot",null)),s?(0,r.h)("div",{class:"transition-effect"},(0,r.h)("div",{class:"transition-cover"}),(0,r.h)("div",{class:"transition-shadow"})):null,(0,r.h)("slot",{name:"fixed"}))},Object.defineProperty(t.prototype,"el",{get:function(){return(0,r.d)(this)},enumerable:!0,configurable:!0}),Object.defineProperty(t,"style",{get:function(){return':host{--background:var(--ion-background-color,#fff);--color:var(--ion-text-color,#000);--padding-top:0px;--padding-bottom:0px;--padding-start:0px;--padding-end:0px;--keyboard-offset:0px;--offset-top:0px;--offset-bottom:0px;--overflow:auto;display:block;position:relative;-ms-flex:1;flex:1;width:100%;height:100%;margin:0!important;padding:0!important;font-family:var(--ion-font-family,inherit);contain:size style}:host(.ion-color) .inner-scroll{background:var(--ion-color-base);color:var(--ion-color-contrast)}:host(.outer-content){--background:var(--ion-color-step-50,#f2f2f2)}.inner-scroll{left:0;right:0;top:calc(var(--offset-top) * -1);bottom:calc(var(--offset-bottom) * -1);padding-left:var(--padding-start);padding-right:var(--padding-end);padding-top:calc(var(--padding-top) + var(--offset-top));padding-bottom:calc(var(--padding-bottom) + var(--keyboard-offset) + var(--offset-bottom));position:absolute;background:var(--background);color:var(--color);-webkit-box-sizing:border-box;box-sizing:border-box;overflow:hidden}@supports ((-webkit-margin-start:0) or (margin-inline-start:0)) or (-webkit-margin-start:0){.inner-scroll{padding-left:unset;padding-right:unset;-webkit-padding-start:var(--padding-start);padding-inline-start:var(--padding-start);-webkit-padding-end:var(--padding-end);padding-inline-end:var(--padding-end)}}.scroll-x,.scroll-y{-webkit-overflow-scrolling:touch;will-change:scroll-position;-ms-scroll-chaining:none;overscroll-behavior:contain}.scroll-y{-ms-touch-action:pan-y;touch-action:pan-y;overflow-y:var(--overflow)}.scroll-x{-ms-touch-action:pan-x;touch-action:pan-x;overflow-x:var(--overflow)}.scroll-x.scroll-y{-ms-touch-action:auto;touch-action:auto}.overscroll:after,.overscroll:before{position:absolute;width:1px;height:1px;content:""}.overscroll:before{bottom:-1px}.overscroll:after{top:-1px}:host(.content-sizing){contain:none}:host(.content-sizing) .inner-scroll{position:relative}.transition-effect{left:-100%;opacity:0;pointer-events:none}.transition-cover,.transition-effect{position:absolute;width:100%;height:100%}.transition-cover{right:0;background:#000;opacity:.1}.transition-shadow{display:block;position:absolute;right:0;width:10px;height:100%;background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAgCAYAAAAIXrg4AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQ1IDc5LjE2MzQ5OSwgMjAxOC8wOC8xMy0xNjo0MDoyMiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKE1hY2ludG9zaCkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MTE3MDgzRkQ5QTkyMTFFOUEwNzQ5MkJFREE1NUY2MjQiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6MTE3MDgzRkU5QTkyMTFFOUEwNzQ5MkJFREE1NUY2MjQiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoxMTcwODNGQjlBOTIxMUU5QTA3NDkyQkVEQTU1RjYyNCIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoxMTcwODNGQzlBOTIxMUU5QTA3NDkyQkVEQTU1RjYyNCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PmePEuQAAABNSURBVHjaYvz//z8DIxAwMDAwATGMhmFmPDQuOSZks0AMmoJBaQHjkPfB0Lfg/2gQjVow+HPy/yHvg9GiYjQfjMbBqAWjFgy/4hogwADYqwdzxy5BuwAAAABJRU5ErkJggg==);background-repeat:repeat-y;background-size:10px 16px}'},enumerable:!0,configurable:!0}),t}(),l=function(t){var o=t.closest("ion-tabs");return o||(t.closest("ion-app,ion-page,.ion-page,page-inner")||function(t){return t.parentElement?t.parentElement:t.parentNode&&t.parentNode.host?t.parentNode.host:null}(t))},c=function(t,o,n,r){var e=t.currentX,i=t.currentY,l=t.timeStamp,c=o.scrollLeft,s=o.scrollTop,a=n-l;if(r&&(t.startTimeStamp=n,t.startX=c,t.startY=s,t.velocityX=t.velocityY=0),t.timeStamp=n,t.currentX=t.scrollLeft=c,t.currentY=t.scrollTop=s,t.deltaX=c-t.startX,t.deltaY=s-t.startY,a>0&&a<100){var u=(c-e)/a,h=(s-i)/a;t.velocityX=.7*u+.3*t.velocityX,t.velocityY=.7*h+.3*t.velocityY}}},636:(t,o,n)=>{n.d(o,{c:()=>e,g:()=>i,h:()=>r,o:()=>c});var r=function(t,o){return null!==o.closest(t)},e=function(t){var o;return"string"==typeof t&&t.length>0?((o={"ion-color":!0})["ion-color-"+t]=!0,o):void 0},i=function(t){var o={};return function(t){return void 0!==t?(Array.isArray(t)?t:t.split(" ")).filter((function(t){return null!=t})).map((function(t){return t.trim()})).filter((function(t){return""!==t})):[]}(t).forEach((function(t){return o[t]=!0})),o},l=/^[a-z][a-z0-9+\-.]*:/,c=function(t,o,n){return r=void 0,e=void 0,c=function(){var r;return function(t,o){var n,r,e,i,l={label:0,sent:function(){if(1&e[0])throw e[1];return e[1]},trys:[],ops:[]};return i={next:c(0),throw:c(1),return:c(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function c(i){return function(c){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;l;)try{if(n=1,r&&(e=2&i[0]?r.return:i[0]?r.throw||((e=r.return)&&e.call(r),0):r.next)&&!(e=e.call(r,i[1])).done)return e;switch(r=0,e&&(i=[2&i[0],e.value]),i[0]){case 0:case 1:e=i;break;case 4:return l.label++,{value:i[1],done:!1};case 5:l.label++,r=i[1],i=[0];continue;case 7:i=l.ops.pop(),l.trys.pop();continue;default:if(!((e=(e=l.trys).length>0&&e[e.length-1])||6!==i[0]&&2!==i[0])){l=0;continue}if(3===i[0]&&(!e||i[1]>e[0]&&i[1]<e[3])){l.label=i[1];break}if(6===i[0]&&l.label<e[1]){l.label=e[1],e=i;break}if(e&&l.label<e[2]){l.label=e[2],l.ops.push(i);break}e[2]&&l.ops.pop(),l.trys.pop();continue}i=o.call(t,l)}catch(t){i=[6,t],r=0}finally{n=e=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,c])}}}(this,(function(e){return null!=t&&"#"!==t[0]&&!l.test(t)&&(r=document.querySelector("ion-router"))?(null!=o&&o.preventDefault(),[2,r.push(t,n)]):[2,!1]}))},new((i=void 0)||(i=Promise))((function(t,o){function n(t){try{s(c.next(t))}catch(t){o(t)}}function l(t){try{s(c.throw(t))}catch(t){o(t)}}function s(o){o.done?t(o.value):new i((function(t){t(o.value)})).then(n,l)}s((c=c.apply(r,e||[])).next())}));var r,e,i,c}}}]);