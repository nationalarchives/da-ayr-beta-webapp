"use strict";(self.webpackChunkUV=self.webpackChunkUV||[]).push([[1811,3748],{884:(t,e,r)=>{r.d(e,{a:()=>i,b:()=>c,c:()=>a,d:()=>p,e:()=>h,f:()=>o,h:()=>n,i:()=>d,n:()=>u,p:()=>l,r:()=>s});var i=function(t){return"function"==typeof __zone_symbol__requestAnimationFrame?__zone_symbol__requestAnimationFrame(t):"function"==typeof requestAnimationFrame?requestAnimationFrame(t):setTimeout(t)},n=function(t){return!!t.shadowRoot&&!!t.attachShadow},o=function(t){var e=t.closest("ion-item");return e?e.querySelector("ion-label"):null},s=function(t,e,r,i,o){if(t||n(e)){var s=e.querySelector("input.aux-input");s||((s=e.ownerDocument.createElement("input")).type="hidden",s.classList.add("aux-input"),e.appendChild(s)),s.disabled=o,s.name=r,s.value=i||""}},a=function(t,e,r){return Math.max(t,Math.min(e,r))},c=function(t,e){if(!t){var r="ASSERT: "+e;throw console.error(r),new Error(r)}},u=function(t){return t.timeStamp||Date.now()},l=function(t){if(t){var e=t.changedTouches;if(e&&e.length>0){var r=e[0];return{x:r.clientX,y:r.clientY}}if(void 0!==t.pageX)return{x:t.pageX,y:t.pageY}}return{x:0,y:0}},d=function(t){var e="rtl"===document.dir;switch(t){case"start":return e;case"end":return!e;default:throw new Error('"'+t+'" is not a valid value for [side]. Use "start" or "end" instead.')}},p=function(t,e){var r=t._original||t;return{_original:t,emit:h(r.emit.bind(r),e)}},h=function(t,e){var r;return void 0===e&&(e=0),function(){for(var i=[],n=0;n<arguments.length;n++)i[n]=arguments[n];clearTimeout(r),r=setTimeout.apply(void 0,[t,e].concat(i))}}},3748:(t,e,r)=>{r.r(e),r.d(e,{GESTURE_CONTROLLER:()=>c,createGesture:()=>p});var i,n=function(){function t(){this.gestureId=0,this.requestedStart=new Map,this.disabledGestures=new Map,this.disabledScroll=new Set}return t.prototype.createGesture=function(t){return new o(this,this.newID(),t.name,t.priority||0,!!t.disableScroll)},t.prototype.createBlocker=function(t){return void 0===t&&(t={}),new s(this,this.newID(),t.disable,!!t.disableScroll)},t.prototype.start=function(t,e,r){return this.canStart(t)?(this.requestedStart.set(e,r),!0):(this.requestedStart.delete(e),!1)},t.prototype.capture=function(t,e,r){if(!this.start(t,e,r))return!1;var i=this.requestedStart,n=-1e4;if(i.forEach((function(t){n=Math.max(n,t)})),n===r){this.capturedId=e,i.clear();var o=new CustomEvent("ionGestureCaptured",{detail:{gestureName:t}});return document.dispatchEvent(o),!0}return i.delete(e),!1},t.prototype.release=function(t){this.requestedStart.delete(t),this.capturedId===t&&(this.capturedId=void 0)},t.prototype.disableGesture=function(t,e){var r=this.disabledGestures.get(t);void 0===r&&(r=new Set,this.disabledGestures.set(t,r)),r.add(e)},t.prototype.enableGesture=function(t,e){var r=this.disabledGestures.get(t);void 0!==r&&r.delete(e)},t.prototype.disableScroll=function(t){this.disabledScroll.add(t),1===this.disabledScroll.size&&document.body.classList.add(a)},t.prototype.enableScroll=function(t){this.disabledScroll.delete(t),0===this.disabledScroll.size&&document.body.classList.remove(a)},t.prototype.canStart=function(t){return void 0===this.capturedId&&!this.isDisabled(t)},t.prototype.isCaptured=function(){return void 0!==this.capturedId},t.prototype.isScrollDisabled=function(){return this.disabledScroll.size>0},t.prototype.isDisabled=function(t){var e=this.disabledGestures.get(t);return!!(e&&e.size>0)},t.prototype.newID=function(){return this.gestureId++,this.gestureId},t}(),o=function(){function t(t,e,r,i,n){this.id=e,this.name=r,this.disableScroll=n,this.priority=1e6*i+e,this.ctrl=t}return t.prototype.canStart=function(){return!!this.ctrl&&this.ctrl.canStart(this.name)},t.prototype.start=function(){return!!this.ctrl&&this.ctrl.start(this.name,this.id,this.priority)},t.prototype.capture=function(){if(!this.ctrl)return!1;var t=this.ctrl.capture(this.name,this.id,this.priority);return t&&this.disableScroll&&this.ctrl.disableScroll(this.id),t},t.prototype.release=function(){this.ctrl&&(this.ctrl.release(this.id),this.disableScroll&&this.ctrl.enableScroll(this.id))},t.prototype.destroy=function(){this.release(),this.ctrl=void 0},t}(),s=function(){function t(t,e,r,i){this.id=e,this.disable=r,this.disableScroll=i,this.ctrl=t}return t.prototype.block=function(){if(this.ctrl){if(this.disable)for(var t=0,e=this.disable;t<e.length;t++){var r=e[t];this.ctrl.disableGesture(r,this.id)}this.disableScroll&&this.ctrl.disableScroll(this.id)}},t.prototype.unblock=function(){if(this.ctrl){if(this.disable)for(var t=0,e=this.disable;t<e.length;t++){var r=e[t];this.ctrl.enableGesture(r,this.id)}this.disableScroll&&this.ctrl.enableScroll(this.id)}},t.prototype.destroy=function(){this.unblock(),this.ctrl=void 0},t}(),a="backdrop-no-scroll",c=new n,u=function(t,e,r,i){var n,o,s=l(t)?{capture:!!i.capture,passive:!!i.passive}:!!i.capture;return t.__zone_symbol__addEventListener?(n="__zone_symbol__addEventListener",o="__zone_symbol__removeEventListener"):(n="addEventListener",o="removeEventListener"),t[n](e,r,s),function(){t[o](e,r,s)}},l=function(t){if(void 0===i)try{var e=Object.defineProperty({},"passive",{get:function(){i=!0}});t.addEventListener("optsTest",(function(){}),e)}catch(t){i=!1}return!!i},d=function(t){return t instanceof Document?t:t.ownerDocument},p=function(t){var e=!1,r=!1,i=!0,n=!1,o=Object.assign({disableScroll:!1,direction:"x",gesturePriority:0,passive:!0,maxAngle:40,threshold:10},t),s=o.canStart,a=o.onWillStart,l=o.onStart,p=o.onEnd,v=o.notCaptured,m=o.onMove,y=o.threshold,S={type:"pan",startX:0,startY:0,startTimeStamp:0,currentX:0,currentY:0,velocityX:0,velocityY:0,deltaX:0,deltaY:0,timeStamp:0,event:void 0,data:void 0},g=function(t,e,r){var i=r*(Math.PI/180),n="x"===t,o=Math.cos(i),s=e*e,a=0,c=0,u=!1,l=0;return{start:function(t,e){a=t,c=e,l=0,u=!0},detect:function(t,e){if(!u)return!1;var r=t-a,i=e-c,d=r*r+i*i;if(d<s)return!1;var p=Math.sqrt(d),h=(n?r:i)/p;return l=h>o?1:h<-o?-1:0,u=!1,!0},isGesture:function(){return 0!==l},getDirection:function(){return l}}}(o.direction,o.threshold,o.maxAngle),k=c.createGesture({name:t.gestureName,priority:t.gesturePriority,disableScroll:t.disableScroll}),_=function(){e&&(n=!1,m&&m(S))},w=function(){return!(k&&!k.capture()||(e=!0,i=!1,S.startX=S.currentX,S.startY=S.currentY,S.startTimeStamp=S.timeStamp,a?a(S).then(X):X(),0))},X=function(){l&&l(S),i=!0},Y=function(){e=!1,r=!1,n=!1,i=!0,k.release()},T=function(t){var r=e,n=i;Y(),n&&(h(S,t),r?p&&p(S):v&&v(S))},E=function(t,e,r,i,n){var o,s,a,c,l,p,h,f=0,b=function(i){f=Date.now()+2e3,e(i)&&(!s&&r&&(s=u(t,"touchmove",r,n)),a||(a=u(t,"touchend",m,n)),c||(c=u(t,"touchcancel",m,n)))},v=function(i){f>Date.now()||e(i)&&(!p&&r&&(p=u(d(t),"mousemove",r,n)),h||(h=u(d(t),"mouseup",y,n)))},m=function(t){S(),i&&i(t)},y=function(t){g(),i&&i(t)},S=function(){s&&s(),a&&a(),c&&c(),s=a=c=void 0},g=function(){p&&p(),h&&h(),p=h=void 0},k=function(){S(),g()},_=function(e){e?(o&&o(),l&&l(),o=l=void 0,k()):(o||(o=u(t,"touchstart",b,n)),l||(l=u(t,"mousedown",v,n)))};return{setDisabled:_,stop:k,destroy:function(){_(!0),i=r=e=void 0}}}(o.el,(function(t){var e=b(t);return!(r||!i)&&(f(t,S),S.startX=S.currentX,S.startY=S.currentY,S.startTimeStamp=S.timeStamp=e,S.velocityX=S.velocityY=S.deltaX=S.deltaY=0,S.event=t,(!s||!1!==s(S))&&(k.release(),!!k.start()&&(r=!0,0===y?w():(g.start(S.startX,S.startY),!0))))}),(function(t){e?!n&&i&&(n=!0,h(S,t),requestAnimationFrame(_)):(h(S,t),g.detect(S.currentX,S.currentY)&&(g.isGesture()&&w()||D()))}),T,{capture:!1}),D=function(){Y(),E.stop(),v&&v(S)};return{setDisabled:function(t){t&&e&&T(void 0),E.setDisabled(t)},destroy:function(){k.destroy(),E.destroy()}}},h=function(t,e){if(e){var r=t.currentX,i=t.currentY,n=t.timeStamp;f(e,t);var o=t.currentX,s=t.currentY,a=(t.timeStamp=b(e))-n;if(a>0&&a<100){var c=(o-r)/a,u=(s-i)/a;t.velocityX=.7*c+.3*t.velocityX,t.velocityY=.7*u+.3*t.velocityY}t.deltaX=o-t.startX,t.deltaY=s-t.startY,t.event=e}},f=function(t,e){var r=0,i=0;if(t){var n=t.changedTouches;if(n&&n.length>0){var o=n[0];r=o.clientX,i=o.clientY}else void 0!==t.pageX&&(r=t.pageX,i=t.pageY)}e.currentX=r,e.currentY=i},b=function(t){return t.timeStamp||Date.now()}},4192:(t,e,r)=>{r.r(e),r.d(e,{ion_backdrop:()=>s});var i=r(5873),n=r(884),o=r(3748),s=function(){function t(t){(0,i.r)(this,t),this.lastClick=-1e4,this.blocker=o.GESTURE_CONTROLLER.createBlocker({disableScroll:!0}),this.visible=!0,this.tappable=!0,this.stopPropagation=!0,this.ionBackdropTap=(0,i.c)(this,"ionBackdropTap",7)}return t.prototype.connectedCallback=function(){this.stopPropagation&&this.blocker.block()},t.prototype.disconnectedCallback=function(){this.blocker.unblock()},t.prototype.onTouchStart=function(t){this.lastClick=(0,n.n)(t),this.emitTap(t)},t.prototype.onMouseDown=function(t){this.lastClick<(0,n.n)(t)-2500&&this.emitTap(t)},t.prototype.emitTap=function(t){this.stopPropagation&&(t.preventDefault(),t.stopPropagation()),this.tappable&&this.ionBackdropTap.emit()},t.prototype.render=function(){var t,e=(0,i.f)(this);return(0,i.h)(i.H,{tabindex:"-1",class:(t={},t[e]=!0,t["backdrop-hide"]=!this.visible,t["backdrop-no-tappable"]=!this.tappable,t)})},Object.defineProperty(t,"style",{get:function(){return":host{left:0;right:0;top:0;bottom:0;display:block;position:absolute;-webkit-transform:translateZ(0);transform:translateZ(0);contain:strict;cursor:pointer;opacity:.01;-ms-touch-action:none;touch-action:none;z-index:2}:host(.backdrop-hide){background:transparent}:host(.backdrop-no-tappable){cursor:auto}:host{background-color:var(--ion-backdrop-color,#000)}"},enumerable:!0,configurable:!0}),t}()}}]);