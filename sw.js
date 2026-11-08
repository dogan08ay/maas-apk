const C='maas-v16',F=['./','./index.html','./manifest.json','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>Promise.all(F.map(u=>c.add(u).catch(()=>{})))))});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
 const q=e.request;
 if(q.method!=='GET'||q.url.includes('?v=')||!q.url.startsWith(self.location.origin))return;
 e.respondWith((async()=>{
  const c=await caches.open(C);
  const yedek=async()=>(await c.match(q))||(q.mode==='navigate'?(await c.match('./index.html'))||(await c.match('./')):null);
  try{
   const r=await Promise.race([fetch(q,{cache:'no-cache'}),new Promise((_,j)=>setTimeout(()=>j(new Error('zaman asimi')),4000))]);
   if(r&&r.ok){e.waitUntil(c.put(q,r.clone()));return r}
   return (await yedek())||r;
  }catch(_){
   return (await yedek())||Response.error();
  }
 })());
});
