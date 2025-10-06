from flask import render_template, request, redirect, url_for

def init_app(app):
    
    products = ['Nike Air Force 1', 'Nike Air Max 1', 'Nike Air Max 90', 'Nike Dunk Low', 'Nike Blazer', 'Nike Cortez', 'Nike Air Jordan 1', 'Nike Air Max 97']
    productlist = [{'Produto': 'Tênis', 'Categoria': 'Casual', 'Modelo': 'Nike Air Force 1', 'Tamanhos': '38, 39, 40, 42'}]
        
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/produtos', methods=['GET','POST'])
    def produtos():
        product = 'Tênis'
        category = 'Casual'
        sizes = [{'Tamanho' : '38'}, 
                {'Tamanho' : '39'},
                {'Tamanho': '40'},
                {'Tamanho': '41'},
                {'Tamanho': '42'},
                {'Tamanho': '43'},
                {'Tamanho': '44'}]
        
        return render_template('catalogo.html', 
                            product=product,
                            category=category,
                            products=products,
                            sizes=sizes)

    @app.route('/novoproduto', methods=['GET','POST'])
    def novoproduto():
        
        # Tratando a requisição POST
        if request.method == 'POST':
            
            if request.form.get('product') and request.form.get('category') and request.form.get('model') and request.form.get('sizes'):
                productlist.append({'Produto': request.form.get('product'), 'Categoria' : request.form.get('category'), 'Modelo': request.form.get('model'), 'Tamanhos': request.form.get('sizes')})
                return redirect(url_for('novoproduto'))
                
        return render_template('cadastro.html', productlist=productlist)