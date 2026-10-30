#include <mutex>
#include <cmath>
#include "peglib.h"
#include "correction.h"

using namespace correction;

namespace {
  class PEGParser {
    public:
      // We are not sure if peglib is threadsafe, so the policy is to lock this
      // parser mutex until we are done with the peg::Ast object
      std::mutex m;
      typedef std::shared_ptr<peg::Ast> AstPtr;

      PEGParser(const char * grammar) {
        parser_.load_grammar(grammar);
        parser_.enable_ast();
        parser_.enable_packrat_parsing();
      };
      AstPtr parse(const std::string_view expression) {
        AstPtr peg_ast;
        int pos;
        std::string msg;
        parser_.log = [&](size_t ln, size_t col, const std::string &themsg) {
          pos = col;
          msg = themsg;
        };
        if ( ! parser_.parse(expression, peg_ast) ) {
          throw std::runtime_error(
            "Failed to parse Formula expression at position " + std::to_string(pos) + ":\n"
            + std::string(expression) + "\n"
            + std::string(pos, ' ') + "^\n"
            + msg
          );
        }
        peg_ast = parser_.optimize_ast(peg_ast);
        return peg_ast;
      };

    private:
      peg::parser parser_;
  };

  PEGParser tformula_parser(R"(
  EXPRESSION  <- ATOM (BINARYOP ATOM)* {
                  precedence
                    L == !=
                    L > < >= <=
                    L - +
                    L / *
                    R ^
                }
  UNARYOP     <- < '-' >
  BINARYOP    <- < '==' | '!=' | '>' | '<' | '>=' | '<=' | '-' | '+' | '/' | '*' | '^' >
  UNARYF      <- < 'log' | 'log10' | 'exp' | 'erf' | 'sqrt' | 'abs' | 'cos' | 'sin' | 'tan' | 'acos' | 'asin' | 'atan' | 'cosh' | 'sinh' | 'tanh' | 'acosh' | 'asinh' | 'atanh' >
  BINARYF     <- < 'atan2' | 'pow' | 'max' | 'min' >
  PARAMETER   <- '[' < [0-9]+ > ']'
  VARIABLE    <- < [xyzt] >
  LITERAL     <- < '-'? [0-9]+ ('.' [0-9]*)? ('e' '-'? [0-9]+)? >
  CALLU       <- UNARYF '(' EXPRESSION ')'
  CALLB       <- BINARYF '(' EXPRESSION ',' EXPRESSION ')'
  ATOM        <- LITERAL / UATOM
  UATOM       <- UNARYOP? ( CALLU / CALLB / NAME / '(' EXPRESSION ')' )
  NAME        <- PARAMETER / VARIABLE
  %whitespace <- [ \t]*
  )");

  struct TranslationContext {
      const std::vector<double>& params;
      const std::vector<size_t>& variableIdx;
      bool bind_parameters;
  };

  FormulaAst translate_tformula_ast(
      const PEGParser::AstPtr ast,
      const TranslationContext& context
      ) {
    if (ast->is_token) {
      if (ast->name == "LITERAL") {
        return {FormulaAst::NodeType::Literal, ast->token_to_number<double>(), {}};
      }
      else if (ast->name == "VARIABLE") {
        size_t idx;
        if ( ast->token == "x" ) idx = 0;
        else if ( ast->token == "y" ) idx = 1;
        else if ( ast->token == "z" ) idx = 2;
        else if ( ast->token == "t" ) idx = 3;
        else {
          throw std::runtime_error("Unrecognized variable name in formula");
        }
        if ( context.variableIdx.size() <= idx ) {
          throw std::runtime_error("Insufficient variables for formula");
        }
        return {FormulaAst::NodeType::Variable, context.variableIdx[idx], {}};
      }
      else if (ast->name == "PARAMETER") {
        auto pidx = ast->token_to_number<size_t>();
        if ( context.bind_parameters ) {
          if ( pidx >= context.params.size() ) {
            throw std::runtime_error("Insufficient parameters for formula");
          }
          return {FormulaAst::NodeType::Literal, context.params[pidx], {}};
        }
        else {
          return {FormulaAst::NodeType::Parameter, pidx, {}};
        }
      }
    }
    else if (ast->name == "UATOM" ) {
      if ( ast->nodes.size() != 2 ) { throw std::runtime_error("UATOM without 2 nodes?"); }
      auto opname = ast->nodes[0]->token;
      FormulaAst::UnaryOp op;
      if      ( opname == "-" ) { op = FormulaAst::UnaryOp::Negative; }
      else { throw std::runtime_error("Unrecognized unary operation: " + std::string(opname)); }
      return {
        FormulaAst::NodeType::UAtom,
        op,
        {translate_tformula_ast(ast->nodes[1], context)}
      };
    }
    else if (ast->name == "CALLU" ) {
      if ( ast->nodes.size() != 2 ) { throw std::runtime_error("CALLU without 2 nodes?"); }
      FormulaAst::UnaryFcn fun;
      auto name = ast->nodes[0]->token;
      // TODO: lookup in static map
      if      ( name == "log" )   { fun = [](double x) { return std::log(x); }; }
      else if ( name == "log10" ) { fun = [](double x) { return std::log10(x); }; }
      else if ( name == "exp" )   { fun = [](double x) { return std::exp(x); }; }
      else if ( name == "erf" )   { fun = [](double x) { return std::erf(x); }; }
      else if ( name == "sqrt" )  { fun = [](double x) { return std::sqrt(x); }; }
      else if ( name == "abs" )   { fun = [](double x) { return std::abs(x); }; }
      else if ( name == "cos" )   { fun = [](double x) { return std::cos(x); }; }
      else if ( name == "sin" )   { fun = [](double x) { return std::sin(x); }; }
      else if ( name == "tan" )   { fun = [](double x) { return std::tan(x); }; }
      else if ( name == "acos" )  { fun = [](double x) { return std::acos(x); }; }
      else if ( name == "asin" )  { fun = [](double x) { return std::asin(x); }; }
      else if ( name == "atan" )  { fun = [](double x) { return std::atan(x); }; }
      else if ( name == "cosh" )  { fun = [](double x) { return std::cosh(x); }; }
      else if ( name == "sinh" )  { fun = [](double x) { return std::sinh(x); }; }
      else if ( name == "tanh" )  { fun = [](double x) { return std::tanh(x); }; }
      else if ( name == "acosh" ) { fun = [](double x) { return std::acosh(x); }; }
      else if ( name == "asinh" ) { fun = [](double x) { return std::asinh(x); }; }
      else if ( name == "atanh" ) { fun = [](double x) { return std::atanh(x); }; }
      else {
        throw std::runtime_error("unrecognized unary function: " + std::string(name));
      }
      return {
        FormulaAst::NodeType::UnaryCall,
        fun,
        {translate_tformula_ast(ast->nodes[1], context)}
      };
    }
    else if (ast->name == "CALLB" ) {
      if ( ast->nodes.size() != 3 ) { throw std::runtime_error("CALLB without 3 nodes?"); }
      FormulaAst::BinaryFcn fun;
      auto name = ast->nodes[0]->token;
      // TODO: lookup in static map
      if      ( name == "atan2" ) { fun = [](double x, double y) { return std::atan2(x, y); }; }
      else if ( name == "pow" )   { fun = [](double x, double y) { return std::pow(x, y); }; }
      else if ( name == "max" )   { fun = [](double x, double y) { return std::max(x, y); }; }
      else if ( name == "min" )   { fun = [](double x, double y) { return std::min(x, y); }; }
      else {
        throw std::runtime_error("unrecognized binary function: " + std::string(name));
      }
      return {
        FormulaAst::NodeType::BinaryCall,
        fun,
        {translate_tformula_ast(ast->nodes[1], context), translate_tformula_ast(ast->nodes[2], context)}
      };
    }
    else if (ast->name == "EXPRESSION" ) {
      if ( ast->nodes.size() != 3 ) { throw std::runtime_error("EXPRESSION without 3 nodes?"); }
      auto opname = ast->nodes[1]->token;
      FormulaAst::BinaryOp op;
      if      ( opname == "==" ) { op = FormulaAst::BinaryOp::Equal; }
      else if ( opname == "!=" ) { op = FormulaAst::BinaryOp::NotEqual; }
      else if ( opname == ">"  ) { op = FormulaAst::BinaryOp::Greater; }
      else if ( opname == "<"  ) { op = FormulaAst::BinaryOp::Less; }
      else if ( opname == ">=" ) { op = FormulaAst::BinaryOp::GreaterEq; }
      else if ( opname == "<=" ) { op = FormulaAst::BinaryOp::LessEq; }
      else if ( opname == "-"  ) { op = FormulaAst::BinaryOp::Minus; }
      else if ( opname == "+"  ) { op = FormulaAst::BinaryOp::Plus; }
      else if ( opname == "/"  ) { op = FormulaAst::BinaryOp::Div; }
      else if ( opname == "*"  ) { op = FormulaAst::BinaryOp::Times; }
      else if ( opname == "^"  ) { op = FormulaAst::BinaryOp::Pow; }
      else { throw std::runtime_error("Unrecognized binary operation: " + std::string(opname)); }
      return {
        FormulaAst::NodeType::Expression,
        op,
        {translate_tformula_ast(ast->nodes[0], context), translate_tformula_ast(ast->nodes[2], context)}
      };
    }
    throw std::runtime_error("Unrecognized AST node");
  }

}

FormulaAst FormulaAst::parse(
    FormulaAst::ParserType type,
    const std::string_view expression,
    const std::vector<double>& params,
    const std::vector<size_t>& variableIdx,
    bool bind_parameters
    ) {
  if ( type == ParserType::TFormula ) {
    const std::lock_guard<std::mutex> lock(tformula_parser.m);
    return translate_tformula_ast(tformula_parser.parse(expression), TranslationContext{params, variableIdx, bind_parameters});
  }
  throw std::runtime_error("Unrecognized formula parser type");
}

double FormulaAst::evaluate(const std::vector<Variable::Type>& values, const std::vector<double>& params) const {
  switch (nodetype_) {
    case NodeType::Literal:
      return std::get<double>(data_);
    case NodeType::Variable:
      return std::get<double>(values[std::get<size_t>(data_)]);
    case NodeType::Parameter:
      return params[std::get<size_t>(data_)];
    case NodeType::UAtom:
      switch (std::get<UnaryOp>(data_)) {
        case UnaryOp::Negative: return -children_[0].evaluate(values, params);
      }
    case NodeType::UnaryCall:
      return std::get<UnaryFcn>(data_)(
          children_[0].evaluate(values, params)
          );
    case NodeType::BinaryCall:
      return std::get<BinaryFcn>(data_)(
          children_[0].evaluate(values, params), children_[1].evaluate(values, params)
          );
    case NodeType::Undefined:
      throw std::runtime_error("Unrecognized AST node");
    case NodeType::Expression:
      auto left = children_[0].evaluate(values, params);
      auto right = children_[1].evaluate(values, params);
      switch (std::get<BinaryOp>(data_)) {
        case BinaryOp::Equal: return (left == right) ? 1. : 0.;
        case BinaryOp::NotEqual: return (left != right) ? 1. : 0.;
        case BinaryOp::Greater: return (left > right) ? 1. : 0.;
        case BinaryOp::Less: return (left < right) ? 1. : 0.;
        case BinaryOp::GreaterEq: return (left >= right) ? 1. : 0.;
        case BinaryOp::LessEq: return (left <= right) ? 1. : 0.;
        case BinaryOp::Minus: return left - right;
        case BinaryOp::Plus: return left + right;
        case BinaryOp::Div: return left / right;
        case BinaryOp::Times: return left * right;
        case BinaryOp::Pow: return std::pow(left, right);
      };
  }
}
