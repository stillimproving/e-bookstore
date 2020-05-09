const beforePATCH = async (req,res) => {
    if(req.body["$inc"]){
        const book = await db.get("/rest/books/"+req.body._id);
        if(req.body.$inc.Quantity){
            if ((book.Quantity +  req.body.$inc.Quantity) < 0){
                res.end({"error": {field: "Quantity",message:"Not enough quantity", Quantity: book.Quantity}});
            }
        }
    }
    res.end();
}
