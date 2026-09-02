import{STORAGE_KEY}from'./constants.js';import{isEntry}from'./model.js';
/** @param {Storage} storage */
export function loadEntries(storage=localStorage){let raw;try{raw=storage.getItem(STORAGE_KEY)}catch{return{entries:[],error:'Font Crush could not read browser storage. Your board will work for this session, but changes may not survive a refresh.'}}if(!raw)return{entries:[],error:null};try{const data=JSON.parse(raw);if(!Array.isArray(data)||!data.every(isEntry))throw Error();return{entries:data,error:null}}catch{return{entries:[],error:'Saved data was damaged, so Font Crush opened a safe empty board. Your original data was not overwritten.'}}}
/** @param {import('./constants.js').FontEntry[]} entries @param {Storage} storage */
export function saveEntries(entries,storage=localStorage){try{storage.setItem(STORAGE_KEY,JSON.stringify(entries));return null}catch{return'Could not save to browser storage. Keep this tab open and check your privacy or storage settings.'}}
