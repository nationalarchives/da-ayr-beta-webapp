"use strict";(self.webpackChunkUV=self.webpackChunkUV||[]).push([[1718],{8265:(t,e,i)=>{i.d(e,{a:()=>r,b:()=>o,c:()=>s,h:()=>n});var n=function(){var t=window.TapticEngine;t&&t.selection()},r=function(){var t=window.TapticEngine;t&&t.gestureSelectionStart()},o=function(){var t=window.TapticEngine;t&&t.gestureSelectionChanged()},s=function(){var t=window.TapticEngine;t&&t.gestureSelectionEnd()}},884:(t,e,i)=>{i.d(e,{a:()=>n,b:()=>c,c:()=>a,d:()=>u,e:()=>d,f:()=>o,h:()=>r,i:()=>p,n:()=>l,p:()=>h,r:()=>s});var n=function(t){return"function"==typeof __zone_symbol__requestAnimationFrame?__zone_symbol__requestAnimationFrame(t):"function"==typeof requestAnimationFrame?requestAnimationFrame(t):setTimeout(t)},r=function(t){return!!t.shadowRoot&&!!t.attachShadow},o=function(t){var e=t.closest("ion-item");return e?e.querySelector("ion-label"):null},s=function(t,e,i,n,o){if(t||r(e)){var s=e.querySelector("input.aux-input");s||((s=e.ownerDocument.createElement("input")).type="hidden",s.classList.add("aux-input"),e.appendChild(s)),s.disabled=o,s.name=i,s.value=n||""}},a=function(t,e,i){return Math.max(t,Math.min(e,i))},c=function(t,e){if(!t){var i="ASSERT: "+e;throw console.error(i),new Error(i)}},l=function(t){return t.timeStamp||Date.now()},h=function(t){if(t){var e=t.changedTouches;if(e&&e.length>0){var i=e[0];return{x:i.clientX,y:i.clientY}}if(void 0!==t.pageX)return{x:t.pageX,y:t.pageY}}return{x:0,y:0}},p=function(t){var e="rtl"===document.dir;switch(t){case"start":return e;case"end":return!e;default:throw new Error('"'+t+'" is not a valid value for [side]. Use "start" or "end" instead.')}},u=function(t,e){var i=t._original||t;return{_original:t,emit:d(i.emit.bind(i),e)}},d=function(t,e){var i;return void 0===e&&(e=0),function(){for(var n=[],r=0;r<arguments.length;r++)n[r]=arguments[r];clearTimeout(i),i=setTimeout.apply(void 0,[t,e].concat(n))}}},1718:(t,e,i)=>{i.r(e),i.d(e,{ion_picker_column:()=>s});var n=i(5873),r=i(884),o=i(8265),s=function(){function t(t){(0,n.r)(this,t),this.optHeight=0,this.rotateFactor=0,this.scaleFactor=1,this.velocity=0,this.y=0,this.noAnimate=!0,this.ionPickerColChange=(0,n.c)(this,"ionPickerColChange",7)}return t.prototype.colChanged=function(){this.refresh()},t.prototype.connectedCallback=function(){return t=this,e=void 0,o=function(){var t,e,r,o=this;return function(t,e){var i,n,r,o,s={label:0,sent:function(){if(1&r[0])throw r[1];return r[1]},trys:[],ops:[]};return o={next:a(0),throw:a(1),return:a(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function a(o){return function(a){return function(o){if(i)throw new TypeError("Generator is already executing.");for(;s;)try{if(i=1,n&&(r=2&o[0]?n.return:o[0]?n.throw||((r=n.return)&&r.call(n),0):n.next)&&!(r=r.call(n,o[1])).done)return r;switch(n=0,r&&(o=[2&o[0],r.value]),o[0]){case 0:case 1:r=o;break;case 4:return s.label++,{value:o[1],done:!1};case 5:s.label++,n=o[1],o=[0];continue;case 7:o=s.ops.pop(),s.trys.pop();continue;default:if(!((r=(r=s.trys).length>0&&r[r.length-1])||6!==o[0]&&2!==o[0])){s=0;continue}if(3===o[0]&&(!r||o[1]>r[0]&&o[1]<r[3])){s.label=o[1];break}if(6===o[0]&&s.label<r[1]){s.label=r[1],r=o;break}if(r&&s.label<r[2]){s.label=r[2],s.ops.push(o);break}r[2]&&s.ops.pop(),s.trys.pop();continue}o=e.call(t,s)}catch(t){o=[6,t],n=0}finally{i=r=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,a])}}}(this,(function(s){switch(s.label){case 0:return t=0,e=.81,"ios"===(0,n.f)(this)&&(t=-.46,e=1),this.rotateFactor=t,this.scaleFactor=e,r=this,[4,i.e(3748).then(i.bind(i,3748))];case 1:return r.gesture=s.sent().createGesture({el:this.el,gestureName:"picker-swipe",gesturePriority:100,threshold:0,onStart:function(t){return o.onStart(t)},onMove:function(t){return o.onMove(t)},onEnd:function(t){return o.onEnd(t)}}),this.gesture.setDisabled(!1),this.tmrId=setTimeout((function(){o.noAnimate=!1,o.refresh(!0)}),250),[2]}}))},new((r=void 0)||(r=Promise))((function(i,n){function s(t){try{c(o.next(t))}catch(t){n(t)}}function a(t){try{c(o.throw(t))}catch(t){n(t)}}function c(t){t.done?i(t.value):new r((function(e){e(t.value)})).then(s,a)}c((o=o.apply(t,e||[])).next())}));var t,e,r,o},t.prototype.componentDidLoad=function(){var t=this.optsEl;t&&(this.optHeight=t.firstElementChild?t.firstElementChild.clientHeight:0),this.refresh()},t.prototype.disconnectedCallback=function(){cancelAnimationFrame(this.rafId),clearTimeout(this.tmrId),this.gesture&&(this.gesture.destroy(),this.gesture=void 0)},t.prototype.emitColChange=function(){this.ionPickerColChange.emit(this.col)},t.prototype.setSelected=function(t,e){var i=t>-1?-t*this.optHeight:0;this.velocity=0,cancelAnimationFrame(this.rafId),this.update(i,e,!0),this.emitColChange()},t.prototype.update=function(t,e,i){if(this.optsEl){for(var n=0,r=0,s=this.col,c=this.rotateFactor,l=s.selectedIndex=this.indexForY(-t),h=0===e?"":e+"ms",p="scale("+this.scaleFactor+")",u=this.optsEl.children,d=0;d<u.length;d++){var f=u[d],m=s.options[d],g=d*this.optHeight+t,v="";if(0!==c){var y=g*c;Math.abs(y)<=90?(n=0,r=90,v="rotateX("+y+"deg) "):n=-9999}else r=0,n=g;var x=l===d;v+="translate3d(0px,"+n+"px,"+r+"px) ",1===this.scaleFactor||x||(v+=p),this.noAnimate?(m.duration=0,f.style.transitionDuration=""):e!==m.duration&&(m.duration=e,f.style.transitionDuration=h),v!==m.transform&&(m.transform=v,f.style.transform=v),x!==m.selected&&(m.selected=x,x?f.classList.add(a):f.classList.remove(a))}this.col.prevSelected=l,i&&(this.y=t),this.lastIndex!==l&&((0,o.b)(),this.lastIndex=l)}},t.prototype.decelerate=function(){var t=this;if(0!==this.velocity){this.velocity*=c,this.velocity=this.velocity>0?Math.max(this.velocity,1):Math.min(this.velocity,-1);var e=this.y+this.velocity;e>this.minY?(e=this.minY,this.velocity=0):e<this.maxY&&(e=this.maxY,this.velocity=0),this.update(e,0,!0),Math.round(e)%this.optHeight!=0||Math.abs(this.velocity)>1?this.rafId=requestAnimationFrame((function(){return t.decelerate()})):(this.velocity=0,this.emitColChange())}else if(this.y%this.optHeight!=0){var i=Math.abs(this.y%this.optHeight);this.velocity=i>this.optHeight/2?1:-1,this.decelerate()}},t.prototype.indexForY=function(t){return Math.min(Math.max(Math.abs(Math.round(t/this.optHeight)),0),this.col.options.length-1)},t.prototype.onStart=function(t){t.event.preventDefault(),t.event.stopPropagation(),cancelAnimationFrame(this.rafId);for(var e=this.col.options,i=e.length-1,n=0,r=0;r<e.length;r++)e[r].disabled||(i=Math.min(i,r),n=Math.max(n,r));this.minY=-i*this.optHeight,this.maxY=-n*this.optHeight},t.prototype.onMove=function(t){t.event.preventDefault(),t.event.stopPropagation();var e=this.y+t.deltaY;e>this.minY?(e=Math.pow(e,.8),this.bounceFrom=e):e<this.maxY?(e+=Math.pow(this.maxY-e,.9),this.bounceFrom=e):this.bounceFrom=0,this.update(e,0,!1)},t.prototype.onEnd=function(t){if(this.bounceFrom>0)return this.update(this.minY,100,!0),void this.emitColChange();if(this.bounceFrom<0)return this.update(this.maxY,100,!0),void this.emitColChange();if(this.velocity=(0,r.c)(-l,23*t.velocityY,l),0===this.velocity&&0===t.deltaY){var e=t.event.target.closest(".picker-opt");e&&e.hasAttribute("opt-index")&&this.setSelected(parseInt(e.getAttribute("opt-index"),10),h)}else this.y+=t.deltaY,this.decelerate()},t.prototype.refresh=function(t){for(var e=this.col.options.length-1,i=0,n=this.col.options,o=0;o<n.length;o++)n[o].disabled||(e=Math.min(e,o),i=Math.max(i,o));if(0===this.velocity){var s=(0,r.c)(e,this.col.selectedIndex||0,i);if(this.col.prevSelected!==s||t){var a=s*this.optHeight*-1;this.velocity=0,this.update(a,h,!0)}}},t.prototype.render=function(){var t,e=this,i=this.col,r=(0,n.f)(this);return(0,n.h)(n.H,{class:(t={},t[r]=!0,t["picker-col"]=!0,t["picker-opts-left"]="left"===this.col.align,t["picker-opts-right"]="right"===this.col.align,t),style:{"max-width":this.col.columnWidth}},i.prefix&&(0,n.h)("div",{class:"picker-prefix",style:{width:i.prefixWidth}},i.prefix),(0,n.h)("div",{class:"picker-opts",style:{maxWidth:i.optionsWidth},ref:function(t){return e.optsEl=t}},i.options.map((function(t,e){return(0,n.h)("button",{type:"button",class:{"picker-opt":!0,"picker-opt-disabled":!!t.disabled},"opt-index":e},t.text)}))),i.suffix&&(0,n.h)("div",{class:"picker-suffix",style:{width:i.suffixWidth}},i.suffix))},Object.defineProperty(t.prototype,"el",{get:function(){return(0,n.d)(this)},enumerable:!0,configurable:!0}),Object.defineProperty(t,"watchers",{get:function(){return{col:["colChanged"]}},enumerable:!0,configurable:!0}),Object.defineProperty(t,"style",{get:function(){return".picker-col{display:-ms-flexbox;display:flex;position:relative;-ms-flex:1;flex:1;-ms-flex-pack:center;justify-content:center;height:100%;-webkit-box-sizing:content-box;box-sizing:content-box;contain:content}.picker-opts{position:relative;-ms-flex:1;flex:1;max-width:100%}.picker-opt{left:0;top:0;display:block;position:absolute;width:100%;border:0;text-align:center;text-overflow:ellipsis;white-space:nowrap;contain:strict;overflow:hidden;will-change:transform}:host-context([dir=rtl]) .picker-opt,[dir=rtl] .picker-opt{left:unset;right:unset;right:0}.picker-opt.picker-opt-disabled{pointer-events:none}.picker-opt-disabled{opacity:0}.picker-opts-left{-ms-flex-pack:start;justify-content:flex-start}.picker-opts-right{-ms-flex-pack:end;justify-content:flex-end}.picker-opt:active,.picker-opt:focus{outline:none}.picker-prefix{text-align:end}.picker-prefix,.picker-suffix{position:relative;-ms-flex:1;flex:1;white-space:nowrap}.picker-suffix{text-align:start}.picker-col{padding-left:4px;padding-right:4px;padding-top:0;padding-bottom:0;-webkit-transform-style:preserve-3d;transform-style:preserve-3d}@supports ((-webkit-margin-start:0) or (margin-inline-start:0)) or (-webkit-margin-start:0){.picker-col{padding-left:unset;padding-right:unset;-webkit-padding-start:4px;padding-inline-start:4px;-webkit-padding-end:4px;padding-inline-end:4px}}.picker-opts,.picker-prefix,.picker-suffix{top:77px;pointer-events:none}.picker-opt,.picker-opts,.picker-prefix,.picker-suffix{-webkit-transform-style:preserve-3d;transform-style:preserve-3d;color:inherit;font-size:20px;line-height:42px}.picker-opt{padding-left:0;padding-right:0;padding-top:0;padding-bottom:0;margin-left:0;margin-right:0;margin-top:0;margin-bottom:0;-webkit-transform-origin:center center;transform-origin:center center;height:46px;-webkit-transition-timing-function:ease-out;transition-timing-function:ease-out;background:transparent;-webkit-backface-visibility:hidden;backface-visibility:hidden;pointer-events:auto}:host-context([dir=rtl]) .picker-opt,[dir=rtl] .picker-opt{-webkit-transform-origin:calc(100% - center) center;transform-origin:calc(100% - center) center}"},enumerable:!0,configurable:!0}),t}(),a="picker-opt-selected",c=.97,l=90,h=150}}]);