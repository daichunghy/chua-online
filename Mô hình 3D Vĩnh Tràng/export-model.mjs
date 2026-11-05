import * as THREE from 'three';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';
import { readFile, writeFile } from 'node:fs/promises';
globalThis.FileReader=class {readAsArrayBuffer(blob){blob.arrayBuffer().then(v=>{this.result=v;this.onloadend?.()})} readAsDataURL(blob){blob.arrayBuffer().then(v=>{this.result=`data:${blob.type};base64,${Buffer.from(v).toString('base64')}`;this.onloadend?.()})}};
const src=await readFile('main.js','utf8');const body=src.slice(src.indexOf('const world='),src.indexOf('let current='));const scene=new THREE.Scene();const world=Function('THREE','scene',body+'\nreturn world;')(THREE,scene);const result=await new GLTFExporter().parseAsync(world,{binary:true});await writeFile('chua-vinh-trang-phac-thao.glb',Buffer.from(result));console.log('GLB saved',result.byteLength,'bytes');
