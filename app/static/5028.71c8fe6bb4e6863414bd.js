"use strict";(self.webpackChunkUV=self.webpackChunkUV||[]).push([[5028],{5721:(e,t,n)=>{n.d(t,{a:()=>o,d:()=>r});var o=function(e,t,n,o,r){return i=void 0,a=void 0,c=function(){var i;return function(e,t){var n,o,r,i,a={label:0,sent:function(){if(1&r[0])throw r[1];return r[1]},trys:[],ops:[]};return i={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function s(i){return function(s){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,o&&(r=2&i[0]?o.return:i[0]?o.throw||((r=o.return)&&r.call(o),0):o.next)&&!(r=r.call(o,i[1])).done)return r;switch(o=0,r&&(i=[2&i[0],r.value]),i[0]){case 0:case 1:r=i;break;case 4:return a.label++,{value:i[1],done:!1};case 5:a.label++,o=i[1],i=[0];continue;case 7:i=a.ops.pop(),a.trys.pop();continue;default:if(!((r=(r=a.trys).length>0&&r[r.length-1])||6!==i[0]&&2!==i[0])){a=0;continue}if(3===i[0]&&(!r||i[1]>r[0]&&i[1]<r[3])){a.label=i[1];break}if(6===i[0]&&a.label<r[1]){a.label=r[1],r=i;break}if(r&&a.label<r[2]){a.label=r[2],a.ops.push(i);break}r[2]&&a.ops.pop(),a.trys.pop();continue}i=t.call(e,a)}catch(e){i=[6,e],o=0}finally{n=r=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,s])}}}(this,(function(a){switch(a.label){case 0:if(e)return[2,e.attachViewToDom(t,n,r,o)];if("string"!=typeof n&&!(n instanceof HTMLElement))throw new Error("framework delegate is missing");return i="string"==typeof n?t.ownerDocument&&t.ownerDocument.createElement(n):n,o&&o.forEach((function(e){return i.classList.add(e)})),r&&Object.assign(i,r),t.appendChild(i),i.componentOnReady?[4,i.componentOnReady()]:[3,2];case 1:a.sent(),a.label=2;case 2:return[2,i]}}))},new((s=void 0)||(s=Promise))((function(e,t){function n(e){try{r(c.next(e))}catch(e){t(e)}}function o(e){try{r(c.throw(e))}catch(e){t(e)}}function r(t){t.done?e(t.value):new s((function(e){e(t.value)})).then(n,o)}r((c=c.apply(i,a||[])).next())}));var i,a,s,c},r=function(e,t){if(t){if(e){var n=t.parentElement;return e.removeViewFromDom(n,t)}t.remove()}return Promise.resolve()}},1761:(e,t,n)=>{n.d(t,{L:()=>l,a:()=>s,b:()=>c,d:()=>D,g:()=>L,l:()=>k,s:()=>P,t:()=>u});var o=n(5873),r=function(e,t,n,o){return new(n||(n=Promise))((function(r,i){function a(e){try{c(o.next(e))}catch(e){i(e)}}function s(e){try{c(o.throw(e))}catch(e){i(e)}}function c(e){e.done?r(e.value):new n((function(t){t(e.value)})).then(a,s)}c((o=o.apply(e,t||[])).next())}))},i=function(e,t){var n,o,r,i,a={label:0,sent:function(){if(1&r[0])throw r[1];return r[1]},trys:[],ops:[]};return i={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function s(i){return function(s){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,o&&(r=2&i[0]?o.return:i[0]?o.throw||((r=o.return)&&r.call(o),0):o.next)&&!(r=r.call(o,i[1])).done)return r;switch(o=0,r&&(i=[2&i[0],r.value]),i[0]){case 0:case 1:r=i;break;case 4:return a.label++,{value:i[1],done:!1};case 5:a.label++,o=i[1],i=[0];continue;case 7:i=a.ops.pop(),a.trys.pop();continue;default:if(!((r=(r=a.trys).length>0&&r[r.length-1])||6!==i[0]&&2!==i[0])){a=0;continue}if(3===i[0]&&(!r||i[1]>r[0]&&i[1]<r[3])){a.label=i[1];break}if(6===i[0]&&a.label<r[1]){a.label=r[1],r=i;break}if(r&&a.label<r[2]){a.label=r[2],a.ops.push(i);break}r[2]&&a.ops.pop(),a.trys.pop();continue}i=t.call(e,a)}catch(e){i=[6,e],o=0}finally{n=r=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,s])}}},a=void 0,s="ionViewWillLeave",c="ionViewDidLeave",l="ionViewWillUnload",u=function(e){return new Promise((function(t,n){(0,o.w)((function(){p(e),d(e).then((function(n){n.animation&&n.animation.destroy(),f(e),t(n)}),(function(t){f(e),n(t)}))}))}))},p=function(e){var t=e.enteringEl,n=e.leavingEl;S(t,n,e.direction),e.showGoBack?t.classList.add("can-go-back"):t.classList.remove("can-go-back"),P(t,!1),n&&P(n,!1)},d=function(e){return r(a,void 0,void 0,(function(){var t;return i(this,(function(n){switch(n.label){case 0:return[4,v(e)];case 1:return[2,(t=n.sent())?h(t,e):m(e)]}}))}))},f=function(e){var t=e.enteringEl,n=e.leavingEl;t.classList.remove("ion-page-invisible"),void 0!==n&&n.classList.remove("ion-page-invisible")},v=function(e){return r(a,void 0,void 0,(function(){var t;return i(this,(function(o){switch(o.label){case 0:return e.leavingEl&&e.animated&&0!==e.duration?e.animationBuilder?[2,e.animationBuilder]:"ios"!==e.mode?[3,2]:[4,Promise.all([n.e(6653),n.e(5480)]).then(n.bind(n,5480))]:[2,void 0];case 1:return t=o.sent().iosTransitionAnimation,[3,4];case 2:return[4,Promise.all([n.e(6653),n.e(3203)]).then(n.bind(n,3203))];case 3:t=o.sent().mdTransitionAnimation,o.label=4;case 4:return[2,t]}}))}))},h=function(e,t){return r(a,void 0,void 0,(function(){var o,r;return i(this,(function(i){switch(i.label){case 0:return[4,b(t,!0)];case 1:i.sent(),i.label=2;case 2:return i.trys.push([2,5,,6]),[4,n.e(1605).then(n.bind(n,1605))];case 3:return[4,i.sent().create(e,t.baseEl,t)];case 4:return o=i.sent(),[3,6];case 5:return i.sent(),o=e(t.baseEl,t),[3,6];case 6:return g(t.enteringEl,t.leavingEl),[4,w(o,t)];case 7:return r=i.sent(),t.progressCallback&&t.progressCallback(void 0),r&&x(t.enteringEl,t.leavingEl),[2,{hasCompleted:r,animation:o}]}}))}))},m=function(e){return r(a,void 0,void 0,(function(){var t,n;return i(this,(function(o){switch(o.label){case 0:return t=e.enteringEl,n=e.leavingEl,[4,b(e,!1)];case 1:return o.sent(),g(t,n),x(t,n),[2,{hasCompleted:!0}]}}))}))},b=function(e,t){return r(a,void 0,void 0,(function(){var n,o;return i(this,(function(r){switch(r.label){case 0:return n=void 0!==e.deepWait?e.deepWait:t,o=n?[D(e.enteringEl),D(e.leavingEl)]:[E(e.enteringEl),E(e.leavingEl)],[4,Promise.all(o)];case 1:return r.sent(),[4,y(e.viewIsReady,e.enteringEl)];case 2:return r.sent(),[2]}}))}))},y=function(e,t){return r(a,void 0,void 0,(function(){return i(this,(function(n){switch(n.label){case 0:return e?[4,e(t)]:[3,2];case 1:n.sent(),n.label=2;case 2:return[2]}}))}))},w=function(e,t){var n=t.progressCallback,o=new Promise((function(t){e.onFinish((function(n){"number"==typeof n?t(1===n):void 0!==e.hasCompleted&&t(e.hasCompleted)}))}));return n?(e.progressStart(!0),n(e)):e.play(),o},g=function(e,t){k(t,s),k(e,"ionViewWillEnter")},x=function(e,t){k(e,"ionViewDidEnter"),k(t,c)},k=function(e,t){if(e){var n=new CustomEvent(t,{bubbles:!1,cancelable:!1});e.dispatchEvent(n)}},E=function(e){return e&&e.componentOnReady?e.componentOnReady():Promise.resolve()},D=function(e){return r(a,void 0,void 0,(function(){var t;return i(this,(function(n){switch(n.label){case 0:return(t=e)?null==t.componentOnReady?[3,2]:[4,t.componentOnReady()]:[3,4];case 1:if(null!=n.sent())return[2];n.label=2;case 2:return[4,Promise.all(Array.from(t.children).map(D))];case 3:n.sent(),n.label=4;case 4:return[2]}}))}))},P=function(e,t){t?(e.setAttribute("aria-hidden","true"),e.classList.add("ion-page-hidden")):(e.hidden=!1,e.removeAttribute("aria-hidden"),e.classList.remove("ion-page-hidden"))},S=function(e,t,n){void 0!==e&&(e.style.zIndex="back"===n?"99":"101"),void 0!==t&&(t.style.zIndex="100")},L=function(e){return e.classList.contains("ion-page")?e:e.querySelector(":scope > .ion-page, :scope > ion-nav, :scope > ion-tabs")||e}},5028:(e,t,n)=>{n.r(t),n.d(t,{ion_popover:()=>m});var o=n(5873),r=n(636),i=n(1178),a=n(5721),s=n(6653),c=n(1761),l=function(e,t,n,o){return new(n||(n=Promise))((function(r,i){function a(e){try{c(o.next(e))}catch(e){i(e)}}function s(e){try{c(o.throw(e))}catch(e){i(e)}}function c(e){e.done?r(e.value):new n((function(t){t(e.value)})).then(a,s)}c((o=o.apply(e,t||[])).next())}))},u=function(e,t){var n,o,r,i,a={label:0,sent:function(){if(1&r[0])throw r[1];return r[1]},trys:[],ops:[]};return i={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function s(i){return function(s){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,o&&(r=2&i[0]?o.return:i[0]?o.throw||((r=o.return)&&r.call(o),0):o.next)&&!(r=r.call(o,i[1])).done)return r;switch(o=0,r&&(i=[2&i[0],r.value]),i[0]){case 0:case 1:r=i;break;case 4:return a.label++,{value:i[1],done:!1};case 5:a.label++,o=i[1],i=[0];continue;case 7:i=a.ops.pop(),a.trys.pop();continue;default:if(!((r=(r=a.trys).length>0&&r[r.length-1])||6!==i[0]&&2!==i[0])){a=0;continue}if(3===i[0]&&(!r||i[1]>r[0]&&i[1]<r[3])){a.label=i[1];break}if(6===i[0]&&a.label<r[1]){a.label=r[1],r=i;break}if(r&&a.label<r[2]){a.label=r[2],a.ops.push(i);break}r[2]&&a.ops.pop(),a.trys.pop();continue}i=t.call(e,a)}catch(e){i=[6,e],o=0}finally{n=r=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,s])}}},p=function(e,t){var n="top",o="left",r=e.querySelector(".popover-content"),i=r.getBoundingClientRect(),a=i.width,c=i.height,l=e.ownerDocument.defaultView.innerWidth,u=e.ownerDocument.defaultView.innerHeight,p=t&&t.target&&t.target.getBoundingClientRect(),f=null!=p&&"top"in p?p.top:u/2-c/2,v=null!=p&&"left"in p?p.left:l/2,h=p&&p.width||0,m=p&&p.height||0,b=e.querySelector(".popover-arrow"),y=b.getBoundingClientRect(),w=y.width,g=y.height;null==p&&(b.style.display="none");var x={top:f+m,left:v+h/2-w/2},k={top:f+m+(g-1),left:v+h/2-a/2},E=!1,D=!1;k.left<d+25?(E=!0,k.left=d):a+d+k.left+25>l&&(D=!0,k.left=l-a-d,o="right"),f+m+c>u&&f-c>0?(x.top=f-(g+1),k.top=f-c-(g-1),e.className=e.className+" popover-bottom",n="bottom"):f+m+c>u&&(r.style.bottom=d+"%"),b.style.top=x.top+"px",b.style.left=x.left+"px",r.style.top=k.top+"px",r.style.left=k.left+"px",E&&(r.style.left="calc("+k.left+"px + var(--ion-safe-area-left, 0px))"),D&&(r.style.left="calc("+k.left+"px - var(--ion-safe-area-right, 0px))"),r.style.transformOrigin=n+" "+o;var P=(0,s.c)(),S=(0,s.c)(),L=(0,s.c)();return S.addElement(e.querySelector("ion-backdrop")).fromTo("opacity",.01,.08),L.addElement(e.querySelector(".popover-wrapper")).fromTo("opacity",.01,1),P.addElement(e).easing("ease").duration(100).addAnimation([S,L])},d=5,f=function(e){var t=(0,s.c)(),n=(0,s.c)(),o=(0,s.c)();return n.addElement(e.querySelector("ion-backdrop")).fromTo("opacity",.08,0),o.addElement(e.querySelector(".popover-wrapper")).fromTo("opacity",.99,0),t.addElement(e).easing("ease").duration(500).addAnimation([n,o])},v=function(e,t){var n=e.ownerDocument,o="rtl"===n.dir,r="top",i=o?"right":"left",a=e.querySelector(".popover-content"),c=a.getBoundingClientRect(),l=c.width,u=c.height,p=n.defaultView.innerWidth,d=n.defaultView.innerHeight,f=t&&t.target&&t.target.getBoundingClientRect(),v=null!=f&&"bottom"in f?f.bottom:d/2-u/2,h=null!=f&&"left"in f?o?f.left-l+f.width:f.left:p/2-l/2,m=f&&f.height||0,b={top:v,left:h};b.left<12?(b.left=12,i="left"):l+12+b.left>p&&(b.left=p-l-12,i="right"),v+m+u>d&&v-u>0?(b.top=v-u-m,e.className=e.className+" popover-bottom",r="bottom"):v+m+u>d&&(a.style.bottom="12px");var y=(0,s.c)(),w=(0,s.c)(),g=(0,s.c)(),x=(0,s.c)(),k=(0,s.c)();return w.addElement(e.querySelector("ion-backdrop")).fromTo("opacity",.01,.32),g.addElement(e.querySelector(".popover-wrapper")).fromTo("opacity",.01,1),x.addElement(a).beforeStyles({top:b.top+"px",left:b.left+"px","transform-origin":r+" "+i}).fromTo("transform","scale(0.001)","scale(1)"),k.addElement(e.querySelector(".popover-viewport")).fromTo("opacity",.01,1),y.addElement(e).easing("cubic-bezier(0.36,0.66,0.04,1)").duration(300).addAnimation([w,g,x,k])},h=function(e){var t=(0,s.c)(),n=(0,s.c)(),o=(0,s.c)();return n.addElement(e.querySelector("ion-backdrop")).fromTo("opacity",.32,0),o.addElement(e.querySelector(".popover-wrapper")).fromTo("opacity",.99,0),t.addElement(e).easing("ease").duration(500).addAnimation([n,o])},m=function(){function e(e){var t=this;(0,o.r)(this,e),this.presented=!1,this.mode=(0,o.f)(this),this.keyboardClose=!0,this.backdropDismiss=!0,this.showBackdrop=!0,this.translucent=!1,this.animated=!0,this.onDismiss=function(e){e.stopPropagation(),e.preventDefault(),t.dismiss()},this.onBackdropTap=function(){t.dismiss(void 0,i.B)},this.onLifecycle=function(e){var n=t.usersElement,o=b[e.type];if(n&&o){var r=new CustomEvent(o,{bubbles:!1,cancelable:!1,detail:e.detail});n.dispatchEvent(r)}},(0,i.c)(this.el),this.didPresent=(0,o.c)(this,"ionPopoverDidPresent",7),this.willPresent=(0,o.c)(this,"ionPopoverWillPresent",7),this.willDismiss=(0,o.c)(this,"ionPopoverWillDismiss",7),this.didDismiss=(0,o.c)(this,"ionPopoverDidDismiss",7)}return e.prototype.present=function(){return l(this,void 0,void 0,(function(){var e,t,n;return u(this,(function(o){switch(o.label){case 0:if(this.presented)return[2];if(!(e=this.el.querySelector(".popover-content")))throw new Error("container is undefined");return t=Object.assign(Object.assign({},this.componentProps),{popover:this.el}),n=this,[4,(0,a.a)(this.delegate,e,this.component,["popover-viewport",this.el["s-sc"]],t)];case 1:return n.usersElement=o.sent(),[4,(0,c.d)(this.usersElement)];case 2:return o.sent(),[2,(0,i.d)(this,"popoverEnter",p,v,this.event)]}}))}))},e.prototype.dismiss=function(e,t){return l(this,void 0,void 0,(function(){var n;return u(this,(function(o){switch(o.label){case 0:return[4,(0,i.e)(this,e,t,"popoverLeave",f,h,this.event)];case 1:return(n=o.sent())?[4,(0,a.d)(this.delegate,this.usersElement)]:[3,3];case 2:o.sent(),o.label=3;case 3:return[2,n]}}))}))},e.prototype.onDidDismiss=function(){return(0,i.f)(this.el,"ionPopoverDidDismiss")},e.prototype.onWillDismiss=function(){return(0,i.f)(this.el,"ionPopoverWillDismiss")},e.prototype.render=function(){var e,t=(0,o.f)(this),n=this.onLifecycle;return(0,o.h)(o.H,{"aria-modal":"true","no-router":!0,style:{zIndex:""+(2e4+this.overlayIndex)},class:Object.assign(Object.assign({},(0,r.g)(this.cssClass)),(e={},e[t]=!0,e["popover-translucent"]=this.translucent,e)),onIonPopoverDidPresent:n,onIonPopoverWillPresent:n,onIonPopoverWillDismiss:n,onIonPopoverDidDismiss:n,onIonDismiss:this.onDismiss,onIonBackdropTap:this.onBackdropTap},(0,o.h)("ion-backdrop",{tappable:this.backdropDismiss,visible:this.showBackdrop}),(0,o.h)("div",{class:"popover-wrapper"},(0,o.h)("div",{class:"popover-arrow"}),(0,o.h)("div",{class:"popover-content"})))},Object.defineProperty(e.prototype,"el",{get:function(){return(0,o.d)(this)},enumerable:!0,configurable:!0}),Object.defineProperty(e,"style",{get:function(){return'.sc-ion-popover-ios-h{--background:var(--ion-background-color,#fff);--min-width:0;--min-height:0;--max-width:auto;--height:auto;left:0;right:0;top:0;bottom:0;display:-ms-flexbox;display:flex;position:fixed;-ms-flex-align:center;align-items:center;-ms-flex-pack:center;justify-content:center;color:var(--ion-text-color,#000);z-index:1001}.overlay-hidden.sc-ion-popover-ios-h{display:none}.popover-wrapper.sc-ion-popover-ios{opacity:0;z-index:10}.popover-content.sc-ion-popover-ios{display:-ms-flexbox;display:flex;position:absolute;-ms-flex-direction:column;flex-direction:column;width:var(--width);min-width:var(--min-width);max-width:var(--max-width);height:var(--height);min-height:var(--min-height);max-height:var(--max-height);background:var(--background);-webkit-box-shadow:var(--box-shadow);box-shadow:var(--box-shadow);overflow:auto;z-index:10}.popover-viewport.sc-ion-popover-ios{--ion-safe-area-top:0px;--ion-safe-area-right:0px;--ion-safe-area-bottom:0px;--ion-safe-area-left:0px}.sc-ion-popover-ios-h{--width:200px;--max-height:90%;--box-shadow:none}.popover-content.sc-ion-popover-ios{border-radius:10px}.popover-arrow.sc-ion-popover-ios{display:block;position:absolute;width:20px;height:10px;overflow:hidden}.popover-arrow.sc-ion-popover-ios:after{left:3px;top:3px;border-radius:3px;position:absolute;width:14px;height:14px;-webkit-transform:rotate(45deg);transform:rotate(45deg);background:var(--background);content:"";z-index:10}[dir=rtl].sc-ion-popover-ios-h .popover-arrow.sc-ion-popover-ios:after, [dir=rtl] .sc-ion-popover-ios-h .popover-arrow.sc-ion-popover-ios:after, [dir=rtl].sc-ion-popover-ios .popover-arrow.sc-ion-popover-ios:after{left:unset;right:unset;right:3px}.popover-bottom.sc-ion-popover-ios-h .popover-arrow.sc-ion-popover-ios{top:auto;bottom:-10px}.popover-bottom.sc-ion-popover-ios-h .popover-arrow.sc-ion-popover-ios:after{top:-6px}@supports ((-webkit-backdrop-filter:blur(0)) or (backdrop-filter:blur(0))){.popover-translucent.sc-ion-popover-ios-h .popover-arrow.sc-ion-popover-ios:after, .popover-translucent.sc-ion-popover-ios-h .popover-content.sc-ion-popover-ios{background:rgba(var(--ion-background-color-rgb,255,255,255),.8);-webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px)}}'},enumerable:!0,configurable:!0}),e}(),b={ionPopoverDidPresent:"ionViewDidEnter",ionPopoverWillPresent:"ionViewWillEnter",ionPopoverWillDismiss:"ionViewWillLeave",ionPopoverDidDismiss:"ionViewDidLeave"}},1178:(e,t,n)=>{n.d(t,{B:()=>T,a:()=>u,b:()=>l,c:()=>f,d:()=>y,e:()=>w,f:()=>k,g:()=>v,h:()=>m,i:()=>D,j:()=>b,k:()=>p,p:()=>d,s:()=>L});var o=n(5873),r=function(e,t,n,o){return new(n||(n=Promise))((function(r,i){function a(e){try{c(o.next(e))}catch(e){i(e)}}function s(e){try{c(o.throw(e))}catch(e){i(e)}}function c(e){e.done?r(e.value):new n((function(t){t(e.value)})).then(a,s)}c((o=o.apply(e,t||[])).next())}))},i=function(e,t){var n,o,r,i,a={label:0,sent:function(){if(1&r[0])throw r[1];return r[1]},trys:[],ops:[]};return i={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function s(i){return function(s){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,o&&(r=2&i[0]?o.return:i[0]?o.throw||((r=o.return)&&r.call(o),0):o.next)&&!(r=r.call(o,i[1])).done)return r;switch(o=0,r&&(i=[2&i[0],r.value]),i[0]){case 0:case 1:r=i;break;case 4:return a.label++,{value:i[1],done:!1};case 5:a.label++,o=i[1],i=[0];continue;case 7:i=a.ops.pop(),a.trys.pop();continue;default:if(!((r=(r=a.trys).length>0&&r[r.length-1])||6!==i[0]&&2!==i[0])){a=0;continue}if(3===i[0]&&(!r||i[1]>r[0]&&i[1]<r[3])){a.label=i[1];break}if(6===i[0]&&a.label<r[1]){a.label=r[1],r=i;break}if(r&&a.label<r[2]){a.label=r[2],a.ops.push(i);break}r[2]&&a.ops.pop(),a.trys.pop();continue}i=t.call(e,a)}catch(e){i=[6,e],o=0}finally{n=r=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,s])}}},a=void 0,s=0,c=function(e){return{create:function(t){return v(e,t)},dismiss:function(t,n,o){return m(document,t,n,e,o)},getTop:function(){return r(this,void 0,void 0,(function(){return i(this,(function(t){return[2,b(document,e)]}))}))}}},l=c("ion-alert"),u=c("ion-action-sheet"),p=c("ion-picker"),d=c("ion-popover"),f=function(e){var t=document;h(t);var n=s++;e.overlayIndex=n,e.hasAttribute("id")||(e.id="ion-overlay-"+n)},v=function(e,t){return customElements.whenDefined(e).then((function(){var n=document,o=n.createElement(e);return o.classList.add("overlay-hidden"),Object.assign(o,t),g(n).appendChild(o),o.componentOnReady()}))},h=function(e){0===s&&(s=1,e.addEventListener("focusin",(function(t){var n=b(e);if(n&&n.backdropDismiss&&!P(n,t.target)){var o=n.querySelector("input,button");o&&o.focus()}})),e.addEventListener("ionBackButton",(function(t){var n=b(e);n&&n.backdropDismiss&&t.detail.register(100,(function(){return n.dismiss(void 0,T)}))})),e.addEventListener("keyup",(function(t){if("Escape"===t.key){var n=b(e);n&&n.backdropDismiss&&n.dismiss(void 0,T)}})))},m=function(e,t,n,o,r){var i=b(e,o,r);return i?i.dismiss(t,n):Promise.reject("overlay does not exist")},b=function(e,t,n){var o=function(e,t){return void 0===t&&(t="ion-alert,ion-action-sheet,ion-loading,ion-modal,ion-picker,ion-popover,ion-toast"),Array.from(e.querySelectorAll(t)).filter((function(e){return e.overlayIndex>0}))}(e,t);return void 0===n?o[o.length-1]:o.find((function(e){return e.id===n}))},y=function(e,t,n,s,c){return r(a,void 0,void 0,(function(){var r;return i(this,(function(i){switch(i.label){case 0:return e.presented?[2]:(e.presented=!0,e.willPresent.emit(),r=e.enterAnimation?e.enterAnimation:o.i.get(t,"ios"===e.mode?n:s),[4,x(e,r,e.el,c)]);case 1:return i.sent()&&e.didPresent.emit(),[2]}}))}))},w=function(e,t,n,s,c,l,u){return r(a,void 0,void 0,(function(){var r,a;return i(this,(function(i){switch(i.label){case 0:if(!e.presented)return[2,!1];e.presented=!1,i.label=1;case 1:return i.trys.push([1,3,,4]),e.willDismiss.emit({data:t,role:n}),r=e.leaveAnimation?e.leaveAnimation:o.i.get(s,"ios"===e.mode?c:l),[4,x(e,r,e.el,u)];case 2:return i.sent(),e.didDismiss.emit({data:t,role:n}),[3,4];case 3:return a=i.sent(),console.error(a),[3,4];case 4:return e.el.remove(),[2,!0]}}))}))},g=function(e){return e.querySelector("ion-app")||e.body},x=function(e,t,s,c){return r(a,void 0,void 0,(function(){var r,a,l,u,p;return i(this,(function(i){switch(i.label){case 0:if(e.animation)return e.animation.destroy(),e.animation=void 0,[2,!1];s.classList.remove("overlay-hidden"),r=s.shadowRoot||e.el,l=!0,i.label=1;case 1:return i.trys.push([1,4,,5]),[4,n.e(1605).then(n.bind(n,1605))];case 2:return[4,i.sent().create(t,r,c)];case 3:return a=i.sent(),[3,5];case 4:return i.sent(),(a=t(r,c)).fill("both"),l=!1,[3,5];case 5:return e.animation=a,e.animated&&o.i.getBoolean("animated",!0)||a.duration(0),e.keyboardClose&&a.beforeAddWrite((function(){var e=s.ownerDocument.activeElement;e&&e.matches("input, ion-input, ion-textarea")&&e.blur()})),[4,a.playAsync()];case 6:return u=i.sent(),p=void 0===u||a.hasCompleted,l&&a.destroy(),e.animation=void 0,[2,p]}}))}))},k=function(e,t){var n,o=new Promise((function(e){return n=e}));return E(e,t,(function(e){n(e.detail)})),o},E=function(e,t,n){var o=function(r){e.removeEventListener(t,o),n(r)};e.addEventListener(t,o)},D=function(e){return"cancel"===e||e===T},P=function(e,t){for(;t;){if(t===e)return!0;t=t.parentElement}return!1},S=function(e){return e()},L=function(e,t){if("function"==typeof e)return o.i.get("_zoneGate",S)((function(){try{return e(t)}catch(e){console.error(e)}}))},T="backdrop"},636:(e,t,n)=>{n.d(t,{c:()=>r,g:()=>i,h:()=>o,o:()=>s});var o=function(e,t){return null!==t.closest(e)},r=function(e){var t;return"string"==typeof e&&e.length>0?((t={"ion-color":!0})["ion-color-"+e]=!0,t):void 0},i=function(e){var t={};return function(e){return void 0!==e?(Array.isArray(e)?e:e.split(" ")).filter((function(e){return null!=e})).map((function(e){return e.trim()})).filter((function(e){return""!==e})):[]}(e).forEach((function(e){return t[e]=!0})),t},a=/^[a-z][a-z0-9+\-.]*:/,s=function(e,t,n){return o=void 0,r=void 0,s=function(){var o;return function(e,t){var n,o,r,i,a={label:0,sent:function(){if(1&r[0])throw r[1];return r[1]},trys:[],ops:[]};return i={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function s(i){return function(s){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,o&&(r=2&i[0]?o.return:i[0]?o.throw||((r=o.return)&&r.call(o),0):o.next)&&!(r=r.call(o,i[1])).done)return r;switch(o=0,r&&(i=[2&i[0],r.value]),i[0]){case 0:case 1:r=i;break;case 4:return a.label++,{value:i[1],done:!1};case 5:a.label++,o=i[1],i=[0];continue;case 7:i=a.ops.pop(),a.trys.pop();continue;default:if(!((r=(r=a.trys).length>0&&r[r.length-1])||6!==i[0]&&2!==i[0])){a=0;continue}if(3===i[0]&&(!r||i[1]>r[0]&&i[1]<r[3])){a.label=i[1];break}if(6===i[0]&&a.label<r[1]){a.label=r[1],r=i;break}if(r&&a.label<r[2]){a.label=r[2],a.ops.push(i);break}r[2]&&a.ops.pop(),a.trys.pop();continue}i=t.call(e,a)}catch(e){i=[6,e],o=0}finally{n=r=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,s])}}}(this,(function(r){return null!=e&&"#"!==e[0]&&!a.test(e)&&(o=document.querySelector("ion-router"))?(null!=t&&t.preventDefault(),[2,o.push(e,n)]):[2,!1]}))},new((i=void 0)||(i=Promise))((function(e,t){function n(e){try{c(s.next(e))}catch(e){t(e)}}function a(e){try{c(s.throw(e))}catch(e){t(e)}}function c(t){t.done?e(t.value):new i((function(e){e(t.value)})).then(n,a)}c((s=s.apply(o,r||[])).next())}));var o,r,i,s}}}]);