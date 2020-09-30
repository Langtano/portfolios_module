from flask import request, render_template, flash
from portfolios import app, db
from portfolios.forms import NewPortfolioForm
from portfolios.models import Portfolios
from financialInstruments.instruments import (
    StarterPortfolio, ClassicPortfolio, FlexiblePortfolio
)

@app.route('/nuevo-portafolio/', methods=['GET', 'POST'])
def new_portfolio():
    form = NewPortfolioForm()

    if form.validate_on_submit():
        data = form.data
        # Remove unnecessary key-value pair
        data.pop('csrf_token')
        # Merge last names into one field and unpack all remaining info
        portfolio = Portfolios(
            last_name=f"{data.pop('last_name1')} {data.pop('last_name2')}",
            **data
        )
        db.session.add(portfolio)
        db.session.commit()
        
        flash("Nuevo portafolio creado", "info")

    return render_template('portafolios_form.html', form=form)

@app.route('/portafolios/')
def portfolio_demo():
    portfolios_list = []
    for p in Portfolios.query.all():

        if p.portfolio_type == 'starter':
            port = StarterPortfolio(
                category='fixed', startdate=p.start_date.date(),
                enddate=p.end_date.date(), amount=p.amount,
                dynamic=p.pay_method == 'dynamic', period='month'
            )

        elif p.portfolio_type == 'classic':
            port = ClassicPortfolio(
                category='fixed', startdate=p.start_date.date(),
                enddate=p.end_date.date(), amount=p.amount,
                dynamic=p.pay_method == 'dynamic', period='month'
            )

        elif p.portfolio_type == 'flexible':
            port = FlexiblePortfolio(
                category='fixed', startdate=p.start_date.date(),
                enddate=p.end_date.date(), amount=p.amount,
                dynamic=p.pay_method == 'dynamic', period='month'
            )
        # import pdb;pdb.set_trace()
        portfolios_list.append({
            'type': p.portfolio_type,
            'info': port,
            'table': port.amortize().to_dataframe(),
        })

    return render_template('portfolios.html', portfolios=portfolios_list)