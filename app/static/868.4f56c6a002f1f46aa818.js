"use strict";(self.webpackChunkUV=self.webpackChunkUV||[]).push([[868],{868:(o,e,n)=>{n.r(e),n.d(e,{ion_segment:()=>i});var t=n(5873),r=n(636),i=function(){function o(o){(0,t.r)(this,o),this.didInit=!1,this.disabled=!1,this.scrollable=!1,this.ionChange=(0,t.c)(this,"ionChange",7),this.ionStyle=(0,t.c)(this,"ionStyle",7)}return o.prototype.valueChanged=function(o){this.didInit&&(this.updateButtons(),this.ionChange.emit({value:o}))},o.prototype.segmentClick=function(o){var e=o.target;this.value=e.value},o.prototype.connectedCallback=function(){if(void 0===this.value){var o=this.getButtons().find((function(o){return o.checked}));o&&(this.value=o.value)}this.emitStyle()},o.prototype.componentDidLoad=function(){this.updateButtons(),this.didInit=!0},o.prototype.emitStyle=function(){this.ionStyle.emit({segment:!0})},o.prototype.updateButtons=function(){for(var o=this.value,e=0,n=this.getButtons();e<n.length;e++){var t=n[e];t.checked=t.value===o}},o.prototype.getButtons=function(){return Array.from(this.el.querySelectorAll("ion-segment-button"))},o.prototype.render=function(){var o,e=(0,t.f)(this);return(0,t.h)(t.H,{class:Object.assign(Object.assign({},(0,r.c)(this.color)),(o={},o[e]=!0,o["segment-disabled"]=this.disabled,o["segment-scrollable"]=this.scrollable,o))})},Object.defineProperty(o.prototype,"el",{get:function(){return(0,t.d)(this)},enumerable:!0,configurable:!0}),Object.defineProperty(o,"watchers",{get:function(){return{value:["valueChanged"]}},enumerable:!0,configurable:!0}),Object.defineProperty(o,"style",{get:function(){return".sc-ion-segment-md-h{--indicator-color-checked:initial;--ripple-color:currentColor;--color-activated:initial;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;display:-ms-flexbox;display:flex;-ms-flex-align:stretch;align-items:stretch;-ms-flex-pack:center;justify-content:center;width:100%;font-family:var(--ion-font-family,inherit);text-align:center}.sc-ion-segment-md-s > .segment-button-disabled, .segment-disabled.sc-ion-segment-md-h{pointer-events:none}.segment-scrollable.sc-ion-segment-md-h{-ms-flex-pack:start;justify-content:start;width:auto;overflow-x:scroll}.segment-scrollable.sc-ion-segment-md-h::-webkit-scrollbar{display:none}.sc-ion-segment-md-h{--background:none;--background-checked:none;--background-hover:rgba(var(--ion-color-primary-rgb,56,128,255),0.04);--background-activated:rgba(var(--ion-color-primary-rgb,56,128,255),0.16);--color:rgba(var(--ion-text-color-rgb,0,0,0),0.6);--color-checked:var(--ion-color-primary,#3880ff);--color-checked-disabled:var(--color-checked);--indicator-color:transparent}.segment-disabled.sc-ion-segment-md-h{opacity:.3}.sc-ion-segment-md-h.ion-color.sc-ion-segment-md-s > ion-segment-button{--background-activated:rgba(var(--ion-color-base-rgb),0.16);--ripple-color:var(--ion-color-base);background:transparent;color:rgba(var(--ion-text-color-rgb,0,0,0),.6)}.sc-ion-segment-md-h.ion-color.sc-ion-segment-md-s > .segment-button-checked{--indicator-color-checked:var(--ion-color-base);color:var(--ion-color-base)}.sc-ion-segment-md-h.ion-color.sc-ion-segment-md-s > .segment-button-checked.activated{color:var(--ion-color-base)}@media (any-hover:hover){.sc-ion-segment-md-h.ion-color.sc-ion-segment-md-s > ion-segment-button:hover{background:rgba(var(--ion-color-base-rgb),.04)}}.sc-ion-segment-md-hion-toolbar:not(.ion-color):not(.ion-color).sc-ion-segment-md-s > ion-segment-button, ion-toolbar:not(.ion-color) .sc-ion-segment-md-h:not(.ion-color).sc-ion-segment-md-s > ion-segment-button{color:var(--ion-toolbar-color-unchecked,var(--color))}.sc-ion-segment-md-hion-toolbar:not(.ion-color):not(.ion-color).sc-ion-segment-md-s > .segment-button-checked, ion-toolbar:not(.ion-color) .sc-ion-segment-md-h:not(.ion-color).sc-ion-segment-md-s > .segment-button-checked{--indicator-color-checked:var(--ion-toolbar-color-checked,var(--color-checked));color:var(--ion-toolbar-color-checked,var(--color-checked))}.sc-ion-segment-md-hion-toolbar.ion-color:not(.ion-color).sc-ion-segment-md-s > ion-segment-button, ion-toolbar.ion-color .sc-ion-segment-md-h:not(.ion-color).sc-ion-segment-md-s > ion-segment-button{--background-hover:rgba(var(--ion-color-contrast-rgb),0.04);--background-activated:var(--ion-color-base);--color:rgba(var(--ion-color-contrast-rgb),0.6);--color-checked:var(--ion-color-contrast);--indicator-color-checked:var(--ion-color-contrast)}"},enumerable:!0,configurable:!0}),o}()},636:(o,e,n)=>{n.d(e,{c:()=>r,g:()=>i,h:()=>t,o:()=>a});var t=function(o,e){return null!==e.closest(o)},r=function(o){var e;return"string"==typeof o&&o.length>0?((e={"ion-color":!0})["ion-color-"+o]=!0,e):void 0},i=function(o){var e={};return function(o){return void 0!==o?(Array.isArray(o)?o:o.split(" ")).filter((function(o){return null!=o})).map((function(o){return o.trim()})).filter((function(o){return""!==o})):[]}(o).forEach((function(o){return e[o]=!0})),e},c=/^[a-z][a-z0-9+\-.]*:/,a=function(o,e,n){return t=void 0,r=void 0,a=function(){var t;return function(o,e){var n,t,r,i,c={label:0,sent:function(){if(1&r[0])throw r[1];return r[1]},trys:[],ops:[]};return i={next:a(0),throw:a(1),return:a(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function a(i){return function(a){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;c;)try{if(n=1,t&&(r=2&i[0]?t.return:i[0]?t.throw||((r=t.return)&&r.call(t),0):t.next)&&!(r=r.call(t,i[1])).done)return r;switch(t=0,r&&(i=[2&i[0],r.value]),i[0]){case 0:case 1:r=i;break;case 4:return c.label++,{value:i[1],done:!1};case 5:c.label++,t=i[1],i=[0];continue;case 7:i=c.ops.pop(),c.trys.pop();continue;default:if(!((r=(r=c.trys).length>0&&r[r.length-1])||6!==i[0]&&2!==i[0])){c=0;continue}if(3===i[0]&&(!r||i[1]>r[0]&&i[1]<r[3])){c.label=i[1];break}if(6===i[0]&&c.label<r[1]){c.label=r[1],r=i;break}if(r&&c.label<r[2]){c.label=r[2],c.ops.push(i);break}r[2]&&c.ops.pop(),c.trys.pop();continue}i=e.call(o,c)}catch(o){i=[6,o],t=0}finally{n=r=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,a])}}}(this,(function(r){return null!=o&&"#"!==o[0]&&!c.test(o)&&(t=document.querySelector("ion-router"))?(null!=e&&e.preventDefault(),[2,t.push(o,n)]):[2,!1]}))},new((i=void 0)||(i=Promise))((function(o,e){function n(o){try{s(a.next(o))}catch(o){e(o)}}function c(o){try{s(a.throw(o))}catch(o){e(o)}}function s(e){e.done?o(e.value):new i((function(o){o(e.value)})).then(n,c)}s((a=a.apply(t,r||[])).next())}));var t,r,i,a}}}]);