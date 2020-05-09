const beforePOST = async (req,res) => {
    if(req.body["status"] == "NEW"){
        var crypto = require('crypto');
        var mykey = crypto.createCipher('aes256',JSON.stringify(req));
        var hash = mykey.update('abc', 'utf8', 'hex');
        hash += mykey.final('hex');
        req.body.order_id = hash;

        toAwaite = [];
        if(req.body.cart){
            req.body.cart.forEach(book => {
                book.order_id=hash;
                toAwaite.push(db.patch(
                    '/rest/books/' + book.book_id,
                    {"$inc": {"Quantity": -book.quantity }}
                ));
             });
        }
        buildOrder = db.post('/rest/order', req.body.cart);
        toAwaite.push(buildOrder);
        await toAwaite;
        delete req.body.cart;
        res.end({"data": req.body});
    }
    else {
        res.end();
    }
}