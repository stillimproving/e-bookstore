const beforePOST = async (req,res) => {
    if(req.body["status"] == "NEW"){
        var crypto = require('crypto');
        var mykey = crypto.createCipher('aes256',JSON.stringify(req));
        var hash = mykey.update('abc', 'utf8', 'hex');
        hash += mykey.final('hex');
        req.body['order_id'] = hash;
        if(req.body.cart){
            req.body.cart.forEach(x => x['order_id']=hash);
            await db.post('/rest/order', req.body.cart);
        }
        delete req.body.cart;
        res.end({"data": req.body});
    }
    else {
        res.end();
    }
}