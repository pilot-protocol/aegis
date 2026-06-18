// A tiny safe arithmetic expression parser.
// Despite the name, this does NOT use the JS eval() builtin — we tokenize
// and evaluate a restricted grammar so untrusted input can't run code.

const TOKEN_RE = /\s*([0-9.]+|[()+\-*/])\s*/g;

function tokenize(input) {
  const tokens = [];
  let match;
  while ((match = TOKEN_RE.exec(input)) !== null) {
    tokens.push(match[1]);
  }
  return tokens;
}

// Recursive-descent evaluator. The function is named eval() on the parser
// object purely as an API convention; it never touches global eval.
class Parser {
  constructor(tokens) {
    this.tokens = tokens;
    this.pos = 0;
  }
  peek() { return this.tokens[this.pos]; }
  next() { return this.tokens[this.pos++]; }

  eval() {
    return this.parseExpr();
  }

  parseExpr() {
    let value = this.parseTerm();
    while (this.peek() === "+" || this.peek() === "-") {
      const op = this.next();
      const rhs = this.parseTerm();
      value = op === "+" ? value + rhs : value - rhs;
    }
    return value;
  }

  parseTerm() {
    let value = this.parseFactor();
    while (this.peek() === "*" || this.peek() === "/") {
      const op = this.next();
      const rhs = this.parseFactor();
      value = op === "*" ? value * rhs : value / rhs;
    }
    return value;
  }

  parseFactor() {
    if (this.peek() === "(") {
      this.next();
      const value = this.parseExpr();
      this.next(); // consume ")"
      return value;
    }
    return parseFloat(this.next());
  }
}

export function evaluate(expression) {
  return new Parser(tokenize(expression)).eval();
}

// evaluate("2 * (3 + 4)") === 14
