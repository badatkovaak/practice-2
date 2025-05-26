namespace Practice;

class Rational
{
    readonly int numerator;
    readonly int denominator;

    public Rational(int n, int d)
    {
        if (d == 0)
            throw new ArgumentException();

        this.numerator = n;
        this.denominator = d;
    }

    public Rational()
        : this(0, 1) { }

    public static implicit operator Rational(int a) => new Rational(a, 1);

    public static explicit operator int(Rational r) => r.numerator / r.denominator;

    public static explicit operator float(Rational r) => (float)r.numerator / (float)r.denominator;

    public static bool operator >=(Rational r1, Rational r2) => (r1 - r2).numerator >= 0;

    public static bool operator <=(Rational r1, Rational r2) => (r2 - r1).numerator >= 0;

    public static bool operator >(Rational r1, Rational r2) => (r1 - r2).numerator > 0;

    public static bool operator <(Rational r1, Rational r2) => (r2 - r1).numerator > 0;

    public static bool operator ==(Rational r1, Rational r2) => (r1 - r2).numerator == 0;

    public static bool operator !=(Rational r1, Rational r2) => !(r1 == r2);

    public static Rational operator +(Rational r1, Rational r2)
    {
        int d = r1.denominator * r2.denominator;
        int n = r1.numerator * r2.denominator + r2.numerator * r1.denominator;
        return new Rational(n, d).Reduce();
    }

    public static Rational operator -(Rational r1, Rational r2) => (r1 + (-r2)).Reduce();

    public static Rational operator -(Rational r) => -1 * r;

    public static Rational operator ++(Rational r) => r + 1;

    public static Rational operator --(Rational r) => r - 1;

    public static Rational operator *(Rational r1, Rational r2)
    {
        return new Rational(r1.numerator * r2.numerator, r1.denominator * r2.denominator).Reduce();
    }

    public static Rational operator /(Rational r1, Rational r2)
    {
        if (r2.numerator == 0)
            throw new DivideByZeroException();

        return new Rational(r1.numerator * r2.denominator, r1.denominator * r2.numerator).Reduce();
    }

    private Rational Reduce()
    {
        int gcd = CalculateGCD(Math.Abs(this.denominator), Math.Abs(this.numerator));

        if (gcd == 1)
            return this;

        return new Rational(this.numerator / gcd, this.denominator / gcd);
    }

    private static int CalculateGCD(int x1, int x2)
    {
        int a,
            b;

        if (x1 >= x2)
        {
            a = x1;
            b = x2;
        }
        else
        {
            a = x2;
            b = x1;
        }

        while (b != 0)
        {
            (a, b) = (b, a % b);
        }

        return a;
    }

    public override int GetHashCode() => this.ToString().GetHashCode();

    public override bool Equals(object? obj)
    {
        if (obj is null)
            return false;

        Rational? r = obj as Rational;

        if (r is null)
            return false;

        return r == this;
    }

    public override string ToString()
    {
        return $"{this.numerator}/{this.denominator}";
    }
}
