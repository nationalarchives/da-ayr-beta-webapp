"use strict";(self.webpackChunkUV=self.webpackChunkUV||[]).push([[980],{980:(e,r,t)=>{t.r(r),t.d(r,{ion_spinner:()=>a});var n=t(5873),i=t(636),s={bubbles:{dur:1e3,circles:9,fn:function(e,r,t){var n=e*r/t-e+"ms",i=2*Math.PI*r/t;return{r:5,style:{top:9*Math.sin(i)+"px",left:9*Math.cos(i)+"px","animation-delay":n}}}},circles:{dur:1e3,circles:8,fn:function(e,r,t){var n=r/t,i=e*n-e+"ms",s=2*Math.PI*n;return{r:5,style:{top:9*Math.sin(s)+"px",left:9*Math.cos(s)+"px","animation-delay":i}}}},circular:{dur:1400,elmDuration:!0,circles:1,fn:function(){return{r:20,cx:44,cy:44,fill:"none",viewBox:"22 22 44 44",transform:"translate(0,0)",style:{}}}},crescent:{dur:750,circles:1,fn:function(){return{r:26,style:{}}}},dots:{dur:750,circles:3,fn:function(e,r){return{r:6,style:{left:9-9*r+"px","animation-delay":-110*r+"ms"}}}},lines:{dur:1e3,lines:12,fn:function(e,r,t){return{y1:17,y2:29,style:{transform:"rotate("+(30*r+(r<6?180:-180))+"deg)","animation-delay":e*r/t-e+"ms"}}}},"lines-small":{dur:1e3,lines:12,fn:function(e,r,t){return{y1:12,y2:20,style:{transform:"rotate("+(30*r+(r<6?180:-180))+"deg)","animation-delay":e*r/t-e+"ms"}}}}},a=function(){function e(e){(0,n.r)(this,e),this.paused=!1}return e.prototype.getName=function(){var e=this.name||n.i.get("spinner"),r=(0,n.f)(this);return e||("ios"===r?"lines":"circular")},e.prototype.render=function(){var e,r=this,t=(0,n.f)(r),a=r.getName(),c=s[a]||s.lines,f="number"==typeof r.duration&&r.duration>10?r.duration:c.dur,u=[];if(void 0!==c.circles)for(var p=0;p<c.circles;p++)u.push(o(c,f,p,c.circles));else if(void 0!==c.lines)for(p=0;p<c.lines;p++)u.push(l(c,f,p,c.lines));return(0,n.h)(n.H,{class:Object.assign(Object.assign({},(0,i.c)(r.color)),(e={},e[t]=!0,e["spinner-"+a]=!0,e["spinner-paused"]=!!r.paused||n.i.getBoolean("_testing"),e)),role:"progressbar",style:c.elmDuration?{animationDuration:f+"ms"}:{}},u)},Object.defineProperty(e,"style",{get:function(){return":host{display:inline-block;position:relative;width:28px;height:28px;color:var(--color);-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}:host(.ion-color){color:var(--ion-color-base)}svg{left:0;top:0;-webkit-transform-origin:center;transform-origin:center;position:absolute;width:100%;height:100%;-webkit-transform:translateZ(0);transform:translateZ(0)}:host-context([dir=rtl]) svg,[dir=rtl] svg{left:unset;right:unset;right:0;-webkit-transform-origin:calc(100% - center);transform-origin:calc(100% - center)}:host(.spinner-lines) line,:host(.spinner-lines-small) line{stroke-width:4px;stroke-linecap:round;stroke:currentColor}:host(.spinner-lines) svg,:host(.spinner-lines-small) svg{-webkit-animation:spinner-fade-out 1s linear infinite;animation:spinner-fade-out 1s linear infinite}:host(.spinner-bubbles) svg{-webkit-animation:spinner-scale-out 1s linear infinite;animation:spinner-scale-out 1s linear infinite;fill:currentColor}:host(.spinner-circles) svg{-webkit-animation:spinner-fade-out 1s linear infinite;animation:spinner-fade-out 1s linear infinite;fill:currentColor}:host(.spinner-crescent) circle{fill:transparent;stroke-width:4px;stroke-dasharray:128px;stroke-dashoffset:82px;stroke:currentColor}:host(.spinner-crescent) svg{-webkit-animation:spinner-rotate 1s linear infinite;animation:spinner-rotate 1s linear infinite}:host(.spinner-dots) circle{stroke-width:0;fill:currentColor}:host(.spinner-dots) svg{-webkit-animation:spinner-dots 1s linear infinite;animation:spinner-dots 1s linear infinite}:host(.spinner-circular){-webkit-animation:spinner-circular linear infinite;animation:spinner-circular linear infinite}:host(.spinner-circular) circle{-webkit-animation:spinner-circular-inner ease-in-out infinite;animation:spinner-circular-inner ease-in-out infinite;stroke:currentColor;stroke-dasharray:80px,200px;stroke-dashoffset:0px;stroke-width:3.6;fill:none}:host(.spinner-paused),:host(.spinner-paused) circle,:host(.spinner-paused) svg{-webkit-animation-play-state:paused;animation-play-state:paused}@-webkit-keyframes spinner-fade-out{0%{opacity:1}to{opacity:0}}@keyframes spinner-fade-out{0%{opacity:1}to{opacity:0}}@-webkit-keyframes spinner-scale-out{0%{-webkit-transform:scale(1);transform:scale(1)}to{-webkit-transform:scale(0);transform:scale(0)}}@keyframes spinner-scale-out{0%{-webkit-transform:scale(1);transform:scale(1)}to{-webkit-transform:scale(0);transform:scale(0)}}@-webkit-keyframes spinner-rotate{0%{-webkit-transform:rotate(0deg);transform:rotate(0deg)}to{-webkit-transform:rotate(1turn);transform:rotate(1turn)}}@keyframes spinner-rotate{0%{-webkit-transform:rotate(0deg);transform:rotate(0deg)}to{-webkit-transform:rotate(1turn);transform:rotate(1turn)}}@-webkit-keyframes spinner-dots{0%{-webkit-transform:scale(1);transform:scale(1);opacity:.9}50%{-webkit-transform:scale(.4);transform:scale(.4);opacity:.3}to{-webkit-transform:scale(1);transform:scale(1);opacity:.9}}@keyframes spinner-dots{0%{-webkit-transform:scale(1);transform:scale(1);opacity:.9}50%{-webkit-transform:scale(.4);transform:scale(.4);opacity:.3}to{-webkit-transform:scale(1);transform:scale(1);opacity:.9}}@-webkit-keyframes spinner-circular{to{-webkit-transform:rotate(1turn);transform:rotate(1turn)}}@keyframes spinner-circular{to{-webkit-transform:rotate(1turn);transform:rotate(1turn)}}@-webkit-keyframes spinner-circular-inner{0%{stroke-dasharray:1px,200px;stroke-dashoffset:0px}50%{stroke-dasharray:100px,200px;stroke-dashoffset:-15px}to{stroke-dasharray:100px,200px;stroke-dashoffset:-125px}}@keyframes spinner-circular-inner{0%{stroke-dasharray:1px,200px;stroke-dashoffset:0px}50%{stroke-dasharray:100px,200px;stroke-dashoffset:-15px}to{stroke-dasharray:100px,200px;stroke-dashoffset:-125px}}"},enumerable:!0,configurable:!0}),e}(),o=function(e,r,t,i){var s=e.fn(r,t,i);return s.style["animation-duration"]=r+"ms",(0,n.h)("svg",{viewBox:s.viewBox||"0 0 64 64",style:s.style},(0,n.h)("circle",{transform:s.transform||"translate(32,32)",cx:s.cx,cy:s.cy,r:s.r,style:e.elmDuration?{animationDuration:r+"ms"}:{}}))},l=function(e,r,t,i){var s=e.fn(r,t,i);return s.style["animation-duration"]=r+"ms",(0,n.h)("svg",{viewBox:s.viewBox||"0 0 64 64",style:s.style},(0,n.h)("line",{transform:"translate(32,32)",y1:s.y1,y2:s.y2}))}},636:(e,r,t)=>{t.d(r,{c:()=>i,g:()=>s,h:()=>n,o:()=>o});var n=function(e,r){return null!==r.closest(e)},i=function(e){var r;return"string"==typeof e&&e.length>0?((r={"ion-color":!0})["ion-color-"+e]=!0,r):void 0},s=function(e){var r={};return function(e){return void 0!==e?(Array.isArray(e)?e:e.split(" ")).filter((function(e){return null!=e})).map((function(e){return e.trim()})).filter((function(e){return""!==e})):[]}(e).forEach((function(e){return r[e]=!0})),r},a=/^[a-z][a-z0-9+\-.]*:/,o=function(e,r,t){return n=void 0,i=void 0,o=function(){var n;return function(e,r){var t,n,i,s,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return s={next:o(0),throw:o(1),return:o(2)},"function"==typeof Symbol&&(s[Symbol.iterator]=function(){return this}),s;function o(s){return function(o){return function(s){if(t)throw new TypeError("Generator is already executing.");for(;a;)try{if(t=1,n&&(i=2&s[0]?n.return:s[0]?n.throw||((i=n.return)&&i.call(n),0):n.next)&&!(i=i.call(n,s[1])).done)return i;switch(n=0,i&&(s=[2&s[0],i.value]),s[0]){case 0:case 1:i=s;break;case 4:return a.label++,{value:s[1],done:!1};case 5:a.label++,n=s[1],s=[0];continue;case 7:s=a.ops.pop(),a.trys.pop();continue;default:if(!((i=(i=a.trys).length>0&&i[i.length-1])||6!==s[0]&&2!==s[0])){a=0;continue}if(3===s[0]&&(!i||s[1]>i[0]&&s[1]<i[3])){a.label=s[1];break}if(6===s[0]&&a.label<i[1]){a.label=i[1],i=s;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(s);break}i[2]&&a.ops.pop(),a.trys.pop();continue}s=r.call(e,a)}catch(e){s=[6,e],n=0}finally{t=i=0}if(5&s[0])throw s[1];return{value:s[0]?s[1]:void 0,done:!0}}([s,o])}}}(this,(function(i){return null!=e&&"#"!==e[0]&&!a.test(e)&&(n=document.querySelector("ion-router"))?(null!=r&&r.preventDefault(),[2,n.push(e,t)]):[2,!1]}))},new((s=void 0)||(s=Promise))((function(e,r){function t(e){try{l(o.next(e))}catch(e){r(e)}}function a(e){try{l(o.throw(e))}catch(e){r(e)}}function l(r){r.done?e(r.value):new s((function(e){e(r.value)})).then(t,a)}l((o=o.apply(n,i||[])).next())}));var n,i,s,o}}}]);